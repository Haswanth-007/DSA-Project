# DSA-Project
Huffman Coding File Compression (DSA Project)
============================================

Overview
--------
This project implements Huffman Coding, a greedy algorithm used for lossless data compression. 
The program reads a text file, compresses it into a binary format, and then decompresses it 
back to verify correctness.

The objective of this project is to understand:
- Tree-based encoding
- Priority queues (min-heaps)
- Bit-level file handling
- Time and space efficiency in compression algorithms


Features
--------
- Reads input text file
- Builds Huffman Tree based on character frequencies
- Generates prefix-free binary codes
- Compresses data into a binary file
- Decompresses back to original text
- Validates correctness of decompression
- Displays:
  * Compression ratio
  * Time performance
  * Space usage
- Graphical visualization:
  * File size comparison
  * Character frequency distribution


Algorithm Used
--------------
Huffman Coding is a greedy algorithm that assigns shorter binary codes to more frequent 
characters and longer codes to less frequent ones.

Steps:
1. Calculate frequency of each character
2. Build a min-heap (priority queue)
3. Construct Huffman Tree
4. Generate binary codes using tree traversal
5. Encode data using generated codes
6. Decode using reconstructed tree


Project Structure
-----------------
.
|-- input.txt              (Input file)
|-- compressed.bin         (Compressed binary file)
|-- decompressed.txt       (Decompressed output file)
|-- main.py                (Main implementation)


How to Run
----------
1. Install dependencies:
   pip install matplotlib

2. Run the program:
   python main.py


Output
------
- Huffman Tree printed in console
- Compression and decompression time
- Compression ratio
- File size comparison graph
- Character frequency distribution graph
- Decompressed file opens automatically


Performance Analysis
--------------------

Time Complexity:
- Frequency Calculation: O(n)
- Building Heap: O(n log n)
- Tree Construction: O(n log n)
- Encoding: O(n)
- Decoding: O(n)

Space Complexity:
- Huffman Tree: O(n)
- Code Table: O(n)
- Output Storage: Depends on compression ratio


Compression Ratio
-----------------
The compression efficiency depends on character distribution:
- High repetition leads to better compression
- Uniform distribution leads to lower compression


Key Concepts Used
-----------------
- Greedy Algorithms
- Binary Trees
- Heap (Priority Queue)
- File Handling (Text and Binary)
- Bit Manipulation


Limitations
-----------
- Works primarily on text files (UTF-8 encoding)
- Additional overhead for storing Huffman codes in file header
- Not optimized for very large files


Future Improvements
-------------------
- Support for larger files and streaming
- GUI-based visualization
- Adaptive Huffman Coding
- Support for other file formats (images, etc.)


Author
------
Haswanth
Madhav
Anuraag
Harish
B.Tech (2nd Year) – IIT Jodhpur
Course: Data Structures & Algorithms


Conclusion
----------
This project demonstrates how theoretical concepts like greedy algorithms and trees are 
applied in real-world systems like file compression. It also highlights trade-offs between 
time, space, and efficiency.
