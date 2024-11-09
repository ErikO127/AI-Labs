import unittest
from Huffman3 import huffman_encoding, huffman_decoding  # Replace with actual module and function names

class TestCompression(unittest.TestCase):
    
    def test_compression(self):
        original_text = "this is a test"
        compressed_file_path = "compressed_test.bin"
        
        # Compress the text
        huffman_encoding(original_text, compressed_file_path)
        
        # Check if the compressed file exists and has some content
        with open(compressed_file_path, 'rb') as f:
            self.assertTrue(len(f.read()) > 0)

    def test_decompression(self):
        original_text = "this is a test"
        compressed_file_path = "compressed_test.bin"
        
        # Compress and then decompress
        huffman_encoding(original_text, compressed_file_path)
        decompressed_text = huffman_decoding(compressed_file_path)
        
        # Ensure decompressed text matches the original
        self.assertEqual(original_text, decompressed_text)

if __name__ == '__main__':
    unittest.main()
