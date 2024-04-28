# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 14:42:58 2024

@author: Anjana
"""

import heapq
import os

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_frequency_table(data):
    frequency_table = {}
    for char in data:
        if char in frequency_table:
            frequency_table[char] += 1
        else:
            frequency_table[char] = 1
    return frequency_table

def build_huffman_tree(frequency_table):
    priority_queue = [HuffmanNode(char, freq) for char, freq in frequency_table.items()]
    heapq.heapify(priority_queue)

    while len(priority_queue) > 1:
        left_node = heapq.heappop(priority_queue)
        right_node = heapq.heappop(priority_queue)

        merged_node = HuffmanNode(None, left_node.freq + right_node.freq)
        merged_node.left = left_node
        merged_node.right = right_node

        heapq.heappush(priority_queue, merged_node)

    return priority_queue[0]

def build_codeword_table(root):
    codeword_table = {}

    def traverse(node, code=''):
        if node:
            if node.char is not None:
                codeword_table[node.char] = code
            traverse(node.left, code + '0')
            traverse(node.right, code + '1')

    traverse(root)
    return codeword_table

def encode(data, codeword_table):
    encoded_data = ''
    for char in data:
        encoded_data += codeword_table[char]
    return encoded_data

def pad_encoded_data(encoded_data):
    padding_amount = 8 - (len(encoded_data) % 8)
    padded_encoded_data = encoded_data + '0' * padding_amount
    padded_encoded_data = format(padding_amount, '08b') + padded_encoded_data
    return padded_encoded_data

def compress(input_file, output_file):
    # Read input data
    with open(input_file, 'r') as file:
        data = file.read()

    # Build Huffman tree
    frequency_table = build_frequency_table(data)
    root = build_huffman_tree(frequency_table)

    # Build codeword table
    codeword_table = build_codeword_table(root)

    # Encode data
    encoded_data = encode(data, codeword_table)

    # Pad encoded data
    padded_encoded_data = pad_encoded_data(encoded_data)

    # Write compressed data to output file
    with open(output_file, 'wb') as file:
        bytes_list = [int(padded_encoded_data[i:i+8], 2) for i in range(0, len(padded_encoded_data), 8)]
        binary_data = bytes(bytes_list)
        file.write(binary_data)

    print("Compression complete.")

def decompress(input_file, output_file):
    # Read compressed data
    with open(input_file, 'rb') as file:
        byte_data = file.read()
    
    # Convert bytes to binary string
    binary_data = ''.join(format(byte, '08b') for byte in byte_data)

    # Read padding amount
    padding_amount = int(binary_data[:8], 2)
    
    # Remove padding
    binary_data = binary_data[8:-padding_amount]

    # Reconstruct Huffman tree
    root = build_huffman_tree(build_frequency_table(binary_data))

    # Decode data
    decoded_data = ''
    current_node = root
    for bit in binary_data:
        if bit == '0':
            current_node = current_node.left
        else:
            current_node = current_node.right
        if current_node.char is not None:
            decoded_data += current_node.char
            current_node = root
    
    # Write decompressed data to output file
    with open(output_file, 'w') as file:
        file.write(decoded_data)

    print("Decompression complete.")
    
    
# Create empty compressed file
with open('compressed.bin', 'wb'):
    pass

# Create empty decompressed file
with open('decompressed.txt', 'w'):
    pass
    

# Example usage:
input_file = 'input.txt'
compressed_file = 'compressed.bin'
decompressed_file = 'decompressed.txt'

# Compress file
compress(input_file, compressed_file)

# Decompress file
decompress(compressed_file, decompressed_file)
