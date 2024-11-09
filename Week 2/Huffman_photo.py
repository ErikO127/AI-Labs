import heapq
from PIL import Image
import numpy as np
from collections import Counter

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
    
    def __lt__(self, other):
        return self.freq < other.freq

def calculate_frequency(data):
    """Calculate frequency of each character or pixel value in the data."""
    return Counter(data)

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

def read_image(file_path):
    img = Image.open(file_path).convert("L")  # Convert to grayscale for simplicity
    img_data = np.array(img).flatten()        # Flatten the image to 1D array
    return img_data, img.size                 # Return both data and dimensions (width, height)

def huffman_encoding(data):
    frequencies = calculate_frequency(data)
    heap = build_priority_queue(frequencies)
    root = build_huffman_tree(heap)
    codes = get_huffman_codes(root)
    encoded_data = ''.join([codes[value] for value in data])
    return encoded_data, root

def huffman_decoding(encoded_data, root):
    decoded_data = []
    current_node = root
    for bit in encoded_data:
        current_node = current_node.left if bit == '0' else current_node.right
        if current_node.left is None and current_node.right is None:
            decoded_data.append(current_node.char)
            current_node = root
    return np.array(decoded_data)

# Usage Example
if __name__ == "__main__":
    # Step 1: Read the image data and get original dimensions
    image_data, (width, height) = read_image("/Users/erikolsson/Desktop/Nice background photos/jpg_44-2.jpg")
    
    # Step 2: Encode the image data
    encoded_data, tree_root = huffman_encoding(image_data)
    print("Encoded image data:", encoded_data[:100], "...")  # Display first 100 bits for preview
    # Write the encoded data to a file
    byte_data = int(encoded_data, 2).to_bytes((len(encoded_data) + 7) // 8, byteorder='big')

    with open("compressed_data.bin", "wb") as file:
        file.write(byte_data)

    
    # Step 3: Decode the image data
    decoded_data = huffman_decoding(encoded_data, tree_root)
    
    # Reshape the 1D decoded data back into the 2D array of the original image dimensions
    decoded_image = decoded_data.reshape((height, width))

    # Display the reconstructed image
    reconstructed_img = Image.fromarray(decoded_image.astype(np.uint8))
    reconstructed_img.show()
