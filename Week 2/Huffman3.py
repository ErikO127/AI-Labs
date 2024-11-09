import heapq
import pickle
from collections import Counter

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
    
    def __lt__(self, other):
        return self.freq < other.freq

def calculate_frequency(text):
    """Calculate frequency of each character in the text."""
    return Counter(text)

def build_priority_queue(frequencies):
    """Build a priority queue from character frequencies."""
    heap = []
    for char, freq in frequencies.items():
        heapq.heappush(heap, Node(char, freq))
    return heap

def build_huffman_tree(heap):
    """Build Huffman Tree from the priority queue."""
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        
        heapq.heappush(heap, merged)
    
    return heap[0]

def generate_codes(root, current_code, codes):
    """Recursively traverse the tree to generate Huffman codes."""
    if root is None:
        return
    
    if root.char is not None:
        codes[root.char] = current_code
    
    generate_codes(root.left, current_code + "0", codes)
    generate_codes(root.right, current_code + "1", codes)

def get_huffman_codes(root):
    """Get Huffman codes for each character."""
    codes = {}
    generate_codes(root, "", codes)
    return codes

def encode_text(text, codes):
    """Encode the text using Huffman codes."""
    encoded_text = "".join([codes[char] for char in text])
    return encoded_text

def pad_encoded_text(encoded_text):
    """Pad encoded text to make its length a multiple of 8 bits."""
    extra_padding = 8 - len(encoded_text) % 8
    for i in range(extra_padding):
        encoded_text += "0"
    padded_info = "{0:08b}".format(extra_padding)
    return padded_info + encoded_text

def get_byte_array(padded_encoded_text):
    """Convert padded encoded text to a byte array."""
    if len(padded_encoded_text) % 8 != 0:
        print("Encoded text not padded properly")
        exit(0)
    
    b = bytearray()
    for i in range(0, len(padded_encoded_text), 8):
        byte = padded_encoded_text[i:i+8]
        b.append(int(byte, 2))
    return b

def huffman_encoding(text, output_path):
    frequencies = calculate_frequency(text)
    heap = build_priority_queue(frequencies)
    root = build_huffman_tree(heap)
    
    codes = get_huffman_codes(root)
    encoded_text = encode_text(text, codes)
    
    padded_encoded_text = pad_encoded_text(encoded_text)
    byte_array = get_byte_array(padded_encoded_text)
    
    with open(output_path, "wb") as file:
        file.write(bytes(byte_array))
        
        with open(f"{output_path}.tree", "wb") as tree_file:
            pickle.dump(root, tree_file)

    print("Compression complete. Compressed data written to:", output_path)

def huffman_decoding(input_path):
    with open(input_path, "rb") as file:
        byte_data = file.read()
    
    with open(f"{input_path}.tree", "rb") as tree_file:
        root = pickle.load(tree_file)
    
    encoded_text = ''.join(f"{byte:08b}" for byte in byte_data)
    
    padded_info = encoded_text[:8]
    extra_padding = int(padded_info, 2)
    encoded_text = encoded_text[8:]  
    encoded_text = encoded_text[:-extra_padding]  
    
    
    decoded_text = ""
    current_node = root
    for bit in encoded_text:
        current_node = current_node.left if bit == "0" else current_node.right
        if current_node.left is None and current_node.right is None:
            decoded_text += current_node.char
            current_node = root
    
    return decoded_text


if __name__ == "__main__":
    with open("words.txt", "r") as file:
        text = file.read()
    
    huffman_encoding(text, "compressed_words.bin")
    
    decompressed_text = huffman_decoding("compressed_words.bin")
    assert text == decompressed_text, "Decompressed text does not match the original!"
    print("Decompression successful and verified.")
    print(decompressed_text)
