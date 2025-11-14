from unittest.mock import Mock, patch
from pathlib import Path
from src.cp import cp
import pytest

class TestCp:
    def setup_method(self):
        self.cp = cp
        self.cwd = Path("/test/cwd")
        self.env = {}

    def test_cp_file(self):
        source = "source.txt"
        dest = "dest.txt"
        with patch('os.path.exists', return_value=True), \
             patch('os.path.isdir', return_value=False), \
             patch('shutil.copy2') as mock_copy, \
             patch('builtins.print') as mock_print, \
             patch('src.cp.log') as mock_log:
            result = self.cp(["cp", source, dest])
            assert result is None
            mock_copy.assert_called_once_with(source, dest)
            mock_print.assert_called_once()
            mock_log.assert_called_once_with("cp source.txt dest.txt", success=True)

    def test_cp_directory_with_r(self):
        source = "source_dir"
        dest = "dest_dir"
        with patch('os.path.exists', return_value=True), \
             patch('os.path.isdir', return_value=True), \
             patch('shutil.copytree') as mock_copytree, \
             patch('builtins.print') as mock_print, \
             patch('src.cp.log') as mock_log:
            result = self.cp(["cp", "-r", source, dest])
            assert result is None
            mock_copytree.assert_called_once_with(source, dest)
            mock_log.assert_called_once_with("cp -r source_dir dest_dir", success=True)

    def test_cp_directory_without_r(self):
        source = "source_dir"
        dest = "dest_dir"
        with patch('os.path.exists', return_value=True), \
             patch('os.path.isdir', return_value=True), \
             patch('builtins.print') as mock_print, \
             patch('src.cp.log') as mock_log:
            result = self.cp(["cp", source, dest])
            assert result is None
            assert mock_print.call_count == 1
            assert "Ошибка" in mock_print.call_args[0][0]
            mock_log.assert_called_once_with("cp source_dir dest_dir", success=False, error="Source is a directory. Use -r for recursive copy")

    def test_cp_not_enough_arguments(self):
        with patch('builtins.print') as mock_print, \
             patch('src.cp.log') as mock_log:
            result = self.cp(["cp"])
            assert result is None
            mock_print.assert_called_once_with("Ошибка: недостаточно аргументов для копирования")
            mock_log.assert_called_once_with("cp", success=False, error="Not enough arguments")

    def test_cp_not_enough_arguments_with_r(self):
        with patch('builtins.print') as mock_print, \
             patch('src.cp.log') as mock_log:
            result = self.cp(["cp", "-r"])
            assert result is None
            mock_print.assert_called_once_with("Ошибка: недостаточно аргументов для рекурсивного копирования")
            mock_log.assert_called_once()

    def test_cp_source_not_found(self):
        source = "nonexistent.txt"
        dest = "dest.txt"
        with patch('os.path.exists', return_value=False), \
             patch('builtins.print') as mock_print, \
             patch('src.cp.log') as mock_log:
            result = self.cp(["cp", source, dest])
            assert result is None
            assert mock_print.call_count == 1
            assert "Ошибка" in mock_print.call_args[0][0]
            mock_log.assert_called_once_with("cp nonexistent.txt dest.txt", success=False, error="Source does not exist")

