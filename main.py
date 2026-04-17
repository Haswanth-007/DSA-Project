#Import libraries
import heapq
import os
import time
import matplotlib.pyplot as plt

#Huffman tree Node definition
class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

    def __repr__(self):
        return f"Node(char={self.char!r}, freq={self.freq})"


#Frequency calculation
def calculate_frequencies(file_path):
    frequencies = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
        for char in text:
            frequencies[char] = frequencies.get(char, 0) + 1
    return frequencies


#build huffman tree
def build_huffman_tree(frequencies):
    priority_queue = []
    for char, freq in frequencies.items():
        heapq.heappush(priority_queue, Node(char, freq))

    if len(priority_queue) == 1:
        node = heapq.heappop(priority_queue)
        new_node = Node(None, node.freq)
        new_node.left = node
        heapq.heappush(priority_queue, new_node)

    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)

        merged_node = Node(None, left.freq + right.freq)
        merged_node.left = left
        merged_node.right = right
        heapq.heappush(priority_queue, merged_node)

    return heapq.heappop(priority_queue)


#Generate huffman code(assign 0, 1 to branches)
def generate_huffman_codes(root):
    codes = {}

    def _traverse(node, current_code):
        if node is None:
            return
        
        if node.char is not None:
            codes[node.char] = current_code
            return

        
        _traverse(node.left, current_code + '0')
       
        _traverse(node.right, current_code + '1')

    _traverse(root, '')
    return codes

def print_huffman_tree(node, indent=""):
    if node is None:
        return

    print_huffman_tree(node.right, indent + "   ")

    if node.char is not None:
        print(indent + f"{node.char}:{node.freq}")
    else:
        print(indent + f"*:{node.freq}")

    print_huffman_tree(node.left, indent + "   ")


#Helper class for bytes->bits
class BitWriter:
    def __init__(self, file_path):
        self.file = open(file_path, 'wb')
        self.buffer = 0
        self.bit_count = 0

    def write_bit(self, bit):
        self.buffer = (self.buffer << 1) | bit
        self.bit_count += 1
        if self.bit_count == 8:
            self.file.write(bytes([self.buffer]))
            self.buffer = 0
            self.bit_count = 0

    def write_byte(self, byte_val):
        for i in range(8):
            bit = (byte_val >> (7 - i)) & 1
            self.write_bit(bit)

    def write_int(self, int_val, num_bytes):
        for i in range(num_bytes):
            self.write_byte((int_val >> (8 * (num_bytes - 1 - i))) & 0xFF)

    def write_code(self, code):
        for bit_char in code:
            self.write_bit(int(bit_char))

    def flush(self):
        if self.bit_count > 0:
            self.buffer <<= (8 - self.bit_count) 
            self.file.write(bytes([self.buffer]))
        self.file.close()

class BitReader:
    def __init__(self, file_path):
        self.file = open(file_path, 'rb')
        self.buffer = 0
        self.bit_count = 0
        self.byte_read = b''

    def _read_next_byte(self):
        self.byte_read = self.file.read(1)
        if self.byte_read:
            self.buffer = self.byte_read[0]
            self.bit_count = 8
            return True
        return False

    def read_bit(self):
        if self.bit_count == 0:
            if not self._read_next_byte():
                return None # End of file

        bit = (self.buffer >> (self.bit_count - 1)) & 1
        self.bit_count -= 1
        return bit

    def read_byte(self):
        byte_val = 0
        for _ in range(8):
            bit = self.read_bit()
            if bit is None:
                return None
            byte_val = (byte_val << 1) | bit
        return byte_val

    def read_int(self, num_bytes):
        int_val = 0
        for _ in range(num_bytes):
            byte_val = self.read_byte()
            if byte_val is None:
                return None
            int_val = (int_val << 8) | byte_val
        return int_val

    def close(self):
        self.file.close()


# Huffman Compression
def huffman_compress_file(input_file_path, output_file_path):
    start_time = time.time()

    # 1. Calculate frequencies
    frequencies = calculate_frequencies(input_file_path)
    if not frequencies:
        print("Input file is empty or cannot be read.")
        return 0

    # 2. Build Huffman Tree ✅
    root = build_huffman_tree(frequencies)

    # 3. Print Huffman Tree ✅
    print("\n--- Huffman Tree ---")
    print_huffman_tree(root)

    # 4. Generate Huffman Codes ✅
    huffman_codes = generate_huffman_codes(root)

    # Read original text
    with open(input_file_path, 'r', encoding='utf-8') as f:
        original_text = f.read()
    original_text_length = len(original_text)

    # 4. Write compressed data to output file
    writer = BitWriter(output_file_path)

    writer.write_int(len(huffman_codes), 2)

    for char, code in huffman_codes.items():
        writer.write_byte(ord(char))
        writer.write_byte(len(code))
        writer.write_code(code)     

    writer.write_int(original_text_length, 8) 

    for char in original_text:
        writer.write_code(huffman_codes[char])

    writer.flush()
    end_time = time.time()
    return end_time - start_time

#Huffman Decompression
def huffman_decompress_file(input_file_path, output_file_path):
    start_time = time.time()

    reader = BitReader(input_file_path)

    num_unique_chars = reader.read_int(2)
    if num_unique_chars is None:
        print("Error: Could not read number of unique characters.")
        reader.close()
        return

    decoded_huffman_codes = {}
    for _ in range(num_unique_chars):
        char_byte = reader.read_byte()
        code_len = reader.read_byte()

        if char_byte is None or code_len is None:
            print("Error: Incomplete Huffman code header.")
            reader.close()
            return

        char = chr(char_byte)
        code_bits = []
        for _ in range(code_len):
            bit = reader.read_bit()
            if bit is None:
                print("Error: Incomplete Huffman code bits.")
                reader.close()
                return
            code_bits.append(str(bit))
        decoded_huffman_codes[''.join(code_bits)] = char

    decode_tree_root = Node(None, None)
    for code, char in decoded_huffman_codes.items():
        current_node = decode_tree_root
        for bit in code:
            if bit == '0':
                if current_node.left is None:
                    current_node.left = Node(None, None)
                current_node = current_node.left
            else: # bit == '1'
                if current_node.right is None:
                    current_node.right = Node(None, None)
                current_node = current_node.right
        current_node.char = char 

    original_text_length = reader.read_int(8)
    if original_text_length is None:
        print("Error: Could not read original text length.")
        reader.close()
        return

    decoded_text = []
    current_node = decode_tree_root
    chars_decoded = 0

    while chars_decoded < original_text_length:
        bit = reader.read_bit()
        if bit is None:
            # This can happen if file is corrupted or original_text_length was wrong
            print(f"Warning: Reached end of compressed data before decoding {original_text_length} characters. Decoded {chars_decoded}.")
            break

        if bit == 0:
            current_node = current_node.left
        else:
            current_node = current_node.right

        if current_node.char is not None: # It's a leaf node
            decoded_text.append(current_node.char)
            chars_decoded += 1
            current_node = decode_tree_root # Reset to root for next character

    reader.close()

    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(''.join(decoded_text))

    end_time = time.time()
    return end_time - start_time

# -------- FILE PATHS --------
input_file = "input.txt"
compressed_file = "compressed.bin"
decompressed_file = "decompressed.txt"

if not os.path.exists(input_file):
        with open(input_file, "w", encoding="utf-8") as f:
            f.write("This is a sample input for Huffman coding project.")
    # Decode the compressed bits

# 2. Perform Compression
print("Compressing file...")
compression_time = huffman_compress_file(input_file, compressed_file)
print(f"Compression finished in {compression_time:.4f} seconds.")

# 3. Perform Decompression
print("Decompressing file...")
decompression_time = huffman_decompress_file(compressed_file, decompressed_file)
print(f"Decompression finished in {decompression_time:.4f} seconds.\n")

# 4. Verify Decompression
original_content = open(input_file, 'r', encoding='utf-8').read()
decompressed_content = open(decompressed_file, 'r', encoding='utf-8').read()

is_match = (original_content == decompressed_content)
print(f"Decompressed content matches original: {is_match}")
print("\n--- Decompressed File Content ---")

with open(decompressed_file, "r", encoding="utf-8") as f:
    print(f.read())

# 5. Calculate Compression Ratio
original_size = os.path.getsize(input_file)
compressed_size = os.path.getsize(compressed_file)

if original_size > 0:
    compression_ratio = (1 - (compressed_size / original_size)) * 100
    print(f"Original file size: {original_size} bytes")
    print(f"Compressed file size: {compressed_size} bytes")
    print(f"Compression Ratio: {compression_ratio:.2f}% reduction")
else:
    print("Original file is empty, cannot calculate compression ratio.")

# 6. Time and Space Analysis (already captured time during execution)
print(f"\nTime Performance:")
print(f"  Compression Time: {compression_time:.4f} seconds")
print(f"  Decompression Time: {decompression_time:.4f} seconds")

print(f"\nSpace Performance:")
print(f"  Original File Space: {original_size} bytes")
print(f"  Compressed File Space: {compressed_size} bytes")
print(f"  Space Saved: {original_size - compressed_size} bytes")

import platform
import subprocess

def open_file(file):
    if platform.system() == "Windows":
        os.startfile(file)
    elif platform.system() == "Darwin":
        subprocess.call(["open", file])
    else:
        subprocess.call(["xdg-open", file])

print("\nOpening decompressed file...")

#Comparision graph
open_file(decompressed_file)
labels = ['Original File', 'Compressed File']
sizes = [original_size, compressed_size]

plt.figure()
plt.bar(labels, sizes)
plt.xlabel("File Type")
plt.ylabel("Size (bytes)")
plt.title("File Size Comparison (Huffman Coding)")
plt.show()

#Frequency distribution graph
frequencies = calculate_frequencies(input_file)

chars = list(frequencies.keys())
freq_values = list(frequencies.values())

plt.figure()
plt.bar(chars, freq_values)
plt.xlabel("Characters")
plt.ylabel("Frequency")
plt.title("Character Frequency Distribution")
plt.xticks(rotation=90)  
plt.show()