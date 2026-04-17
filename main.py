#Import libraries
import heapq
import os
import time

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

    # Modified write_byte to use write_bit for consistency
    def write_byte(self, byte_val):
        for i in range(8):
            bit = (byte_val >> (7 - i)) & 1
            self.write_bit(bit)

    def write_int(self, int_val, num_bytes):
        # Write an integer by breaking it into bytes
        for i in range(num_bytes):
            self.write_byte((int_val >> (8 * (num_bytes - 1 - i))) & 0xFF)

    def write_code(self, code):
        for bit_char in code:
            self.write_bit(int(bit_char))

    def flush(self):
        if self.bit_count > 0:
            self.buffer <<= (8 - self.bit_count) # Pad with zeros
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
                return None # End of file or incomplete byte
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


#Huffman Compression
