from unittest.mock import Mock, patch, mock_open
from pathlib import Path
from src.grep import grep
import pytest

class TestGrep:
    def setup_method(self):
        self.grep = grep
        self.cwd = Path("/test/cwd")
        self.env = {}

    def test_grep_file(self):
        pattern = "test"
        file_path = "test.txt"
        file_content = "line1\ntest line\nline3"
        
        with patch('os.path.exists', return_value=True), \
             patch('os.path.isfile', return_value=True), \
             patch('builtins.open', mock_open(read_data=file_content)), \
             patch('builtins.print') as mock_print:
            result = self.grep(["grep", pattern, file_path])
            assert result is None
            assert mock_print.call_count == 1
            assert "test" in mock_print.call_args[0][0]

    def test_grep_file_with_i_flag(self):
        pattern = "TEST"
        file_path = "test.txt"
        file_content = "line1\ntest line\nline3"
        
        with patch('os.path.exists', return_value=True), \
             patch('os.path.isfile', return_value=True), \
             patch('builtins.open', mock_open(read_data=file_content)), \
             patch('builtins.print') as mock_print:
            result = self.grep(["grep", "-i", pattern, file_path])
            assert result is None
            assert mock_print.call_count == 1

    def test_grep_file_with_r_flag(self):
        pattern = "test"
        file_path = "test.txt"
        file_content = "line1\ntest line\nline3"
        
        with patch('os.path.exists', return_value=True), \
             patch('os.path.isfile', return_value=True), \
             patch('builtins.open', mock_open(read_data=file_content)), \
             patch('builtins.print') as mock_print:
            result = self.grep(["grep", "-r", pattern, file_path])
            assert result is None

    def test_grep_directory(self):
        pattern = "test"
        dir_path = "test_dir"
        
        with patch('os.path.exists', return_value=True), \
             patch('os.path.isfile', return_value=False), \
             patch('os.walk', return_value=[("test_dir", [], ["file1.txt"])]), \
             patch('os.path.join', return_value="test_dir/file1.txt"), \
             patch('builtins.open', mock_open(read_data="test line\nother line")), \
             patch('builtins.print') as mock_print:
            result = self.grep(["grep", pattern, dir_path])
            assert result is None

    def test_grep_not_enough_arguments(self):
        with patch('builtins.print') as mock_print:
            result = self.grep(["grep"])
            assert result is None
            mock_print.assert_called_once_with("Ошибка: недостаточно аргументов. Использование: grep [-r] [-i] pattern path")

    def test_grep_path_not_found(self):
        pattern = "test"
        file_path = "nonexistent.txt"
        
        with patch('os.path.exists', return_value=False), \
             patch('builtins.print') as mock_print:
            result = self.grep(["grep", pattern, file_path])
            assert result is None
            mock_print.assert_called_once_with(f"Ошибка: путь '{file_path}' не найден.")

