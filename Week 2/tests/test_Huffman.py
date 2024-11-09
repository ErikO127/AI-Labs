import unittest
from Huffman import huffman_encoding, huffman_decoding  # Import functions from Huffman.py

class TestHuffman(unittest.TestCase):
    
    def test_compression(self):
        original_text = "this is a test"
        
        # Compress the text
        encoded_text, root = huffman_encoding(original_text)
        
        # Ensure the encoded text is not empty
        self.assertTrue(len(encoded_text) > 0)

    def test_decompression(self):
        original_text = "this is a test"
        
        # Compress and then decompress
        encoded_text, root = huffman_encoding(original_text)
        decompressed_text = huffman_decoding(encoded_text, root)
        
        # Ensure decompressed text matches the original
        self.assertEqual(original_text, decompressed_text)

if __name__ == "__main__":
    unittest.main()
