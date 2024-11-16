def lzw_decompress(input_file, output_file):
    """Decompress a file compressed with the enhanced LZW algorithm."""
    with open(input_file, 'rb') as file:
        compressed_data = []
        while byte := file.read(2):  
            compressed_data.append(int.from_bytes(byte, byteorder='big'))

    dictionary = {i: chr(i) for i in range(256)}
    dict_size = 256

    string = chr(compressed_data.pop(0))
    decompressed_data = [string]

    for code in compressed_data:
        if code in dictionary:
            entry = dictionary[code]
        elif code == dict_size:
            entry = string + string[0]
        else:
            raise ValueError("Invalid compressed data.")
        decompressed_data.append(entry)

        dictionary[dict_size] = string + entry[0]
        dict_size += 1
        string = entry

    with open(output_file, 'w') as file:
        file.write(''.join(decompressed_data))


if __name__ == "__main__":
    compressed_file = "compressed.lzw"
    decompressed_file = "decompressed.txt"

    lzw_decompress(compressed_file, decompressed_file)
