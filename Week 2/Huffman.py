import heapq
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
    encoded_text = ""
    for char in text:
        encoded_text += codes[char]
    return encoded_text

def decode_text(encoded_text, root):
    """Decode the encoded text using the Huffman tree."""
    decoded_text = ""
    current_node = root
    for bit in encoded_text:
        if bit == "0":
            current_node = current_node.left
        else:
            current_node = current_node.right
        
        if current_node.left is None and current_node.right is None:
            decoded_text += current_node.char
            current_node = root 
    return decoded_text

def huffman_encoding(text):
    frequencies = calculate_frequency(text)
    heap = build_priority_queue(frequencies)
    root = build_huffman_tree(heap)
    codes = get_huffman_codes(root)
    encoded_text = encode_text(text, codes)
    return encoded_text, root

def huffman_decoding(encoded_text, root):
    return decode_text(encoded_text, root)

if __name__ == "__main__":

    with open("words.txt", "r") as file:
        text = file.read()
    
    encoded_text, root = huffman_encoding(text)
    print("Encoded text:", encoded_text)
    
    with open("compress_words.txt", "w") as file:
        file.write(encoded_text)

    decoded_text = huffman_decoding(encoded_text, root)
    print("Decoded text:", decoded_text)
    
    assert text == decoded_text, "The decoded text does not match the original!"
