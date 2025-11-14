from unittest.mock import Mock, patch, mock_open
from pathlib import Path
from src.cat import cat
import pytest

class TestCat:
    def setup_method(self):
        self.cat = cat
        self.cwd = Path("/test/cwd")
        self.env = {}

    def test_cat_file(self):
        file_content = "Hello, world!"

        with patch('os.path.exists', return_value=True), \
             patch('os.path.isdir', return_value=False), \
             patch('builtins.open', mock_open(read_data=file_content)), \
             patch('builtins.print') as mock_print, \
             patch('src.cat.log') as mock_log:
            result = self.cat(["cat", "test.txt"])
            assert result is None
            mock_print.assert_called_once_with(file_content)
            mock_log.assert_called_once_with("cat test.txt", success=True)

    def test_cat_no_file_specified(self):
        with patch('builtins.print') as mock_print, \
             patch('src.cat.log') as mock_log:
            result = self.cat(["cat"])
            assert result is None
            mock_print.assert_called_once_with("Ошибка: не указан файл для чтения")
            mock_log.assert_called_once_with("cat", success=False, error="No file specified")

    def test_cat_file_not_found(self):
        with patch('os.path.exists', return_value=False), \
             patch('builtins.print') as mock_print, \
             patch('src.cat.log') as mock_log:
            result = self.cat(["cat", "nonexistent.txt"])
            assert result is None
            assert mock_print.call_count == 1
            assert "Ошибка" in mock_print.call_args[0][0]
            mock_log.assert_called_once()

    def test_cat_directory(self):
        with patch('os.path.exists', return_value=True), \
             patch('os.path.isdir', return_value=True), \
             patch('builtins.print') as mock_print, \
             patch('src.cat.log') as mock_log:
            result = self.cat(["cat", "/some/dir"])
            assert result is None
            assert mock_print.call_count == 1
            assert "Ошибка" in mock_print.call_args[0][0]
            mock_log.assert_called_once()
