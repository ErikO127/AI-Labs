from src.ai_labs_project.UI_implementation import CompressorUI
from unittest.mock import MagicMock
import pytest
from PyQt5.QtCore import Qt

@pytest.fixture
def app(qtbot):
    widget = CompressorUI()
    qtbot.addWidget(widget)
    return widget

def test_ui_compress_words_file(app, qtbot, tmp_path):
    app.text_input.setPlainText(
        """A spectrometric investigation of the correlation between complex ions and their ligands"""
    )

    qtbot.mouseClick(app.compress_button, Qt.LeftButton)

    expected_output = (
        "Original Text Size: 87 bytes\n"
        "Huffman Compressed Size: 45 bytes\n"
        "Lempel-Ziv Compressed Size: 74 bytes\n"
    )
    assert app.text_results.toPlainText() == expected_output

