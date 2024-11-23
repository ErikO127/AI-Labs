from src.ai_labs_project.Lempel_with_compress import lzw_compress
from pathlib import Path
import os

def test_lzw_compress_real_data(tmp_path):
    input_file = tmp_path / "words.txt"
    output_file = tmp_path / "test_output.lzw"

    input_file.write_text(
        "ABABABABABABABABABABABABABABABABABABABABABABABABABABABABABABABABABABABABABAB"
    )

    lzw_compress(str(input_file), str(output_file))

    assert os.path.exists(output_file)

    assert os.path.getsize(output_file) > 0

    assert os.path.getsize(output_file) <= os.path.getsize(input_file)

