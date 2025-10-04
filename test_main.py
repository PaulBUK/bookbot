import os
import stat
import pytest
from main import get_book_text

TEST_BOOK = "books/frankenstein.txt"

def test_read_success():
    text = get_book_text(TEST_BOOK)
    assert isinstance(text, str)
    assert "Frankenstein" in text or "FRANKENSTEIN" in text or len(text) > 100

def test_file_not_found(tmp_path):
    missing = tmp_path / "nope.txt"
    assert get_book_text(str(missing)) is None

def test_permission_denied(tmp_path):
    p = tmp_path / "secret.txt"
    p.write_text("hidden")
    p.chmod(0)
    try:
        assert get_book_text(str(p)) is None
    finally:
        # restore so pytest can clean up
        p.chmod(stat.S_IRUSR | stat.S_IWUSR)

def test_is_directory(tmp_path):
    d = tmp_path / "somedir"
    d.mkdir()
    assert get_book_text(str(d)) is None

def test_unicode_error(tmp_path):
    # create a binary file that will likely raise UnicodeDecodeError when read as utf-8
    b = tmp_path / "binary.dat"
    b.write_bytes(b"\xff\xff\xff\xff\xff")
    assert get_book_text(str(b)) is None
