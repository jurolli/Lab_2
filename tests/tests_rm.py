from unittest.mock import Mock, patch
from pathlib import Path
from src.rm import rm
import pytest

class TestRm:
    def setup_method(self):
        self.rm = rm
        self.cwd = Path("/test/cwd")
        self.env = {}

    def test_rm_file(self):
        file_path = "test.txt"
        with patch('os.path.exists', return_value=True), \
             patch('os.path.isdir', return_value=False), \
             patch('os.remove') as mock_remove, \
             patch('builtins.print') as mock_print, \
             patch('src.rm.log') as mock_log:
            result = self.rm(["rm", file_path])
            assert result is None
            mock_remove.assert_called_once_with(file_path)
            mock_print.assert_called_once()
            mock_log.assert_called_once_with("rm test.txt", success=True)

    def test_rm_directory_with_r(self):
        dir_path = "test_dir"
        with patch('os.path.exists', return_value=True), \
             patch('os.path.isdir', return_value=True), \
             patch('builtins.input', return_value='y'), \
             patch('shutil.rmtree') as mock_rmtree, \
             patch('builtins.print') as mock_print, \
             patch('src.rm.log') as mock_log:
            result = self.rm(["rm", "-r", dir_path])
            assert result is None
            mock_rmtree.assert_called_once_with(dir_path)
            mock_log.assert_called_once_with("rm -r test_dir", success=True)

    def test_rm_directory_without_r(self):
        dir_path = "test_dir"
        with patch('os.path.exists', return_value=True), \
             patch('os.path.isdir', return_value=True), \
             patch('builtins.print') as mock_print, \
             patch('src.rm.log') as mock_log:
            result = self.rm(["rm", dir_path])
            assert result is None
            assert mock_print.call_count == 1
            assert "Ошибка" in mock_print.call_args[0][0]
            mock_log.assert_called_once()

    def test_rm_directory_cancelled(self):
        dir_path = "test_dir"
        with patch('os.path.exists', return_value=True), \
             patch('os.path.isdir', return_value=True), \
             patch('builtins.input', return_value='n'), \
             patch('builtins.print') as mock_print, \
             patch('src.rm.log') as mock_log:
            result = self.rm(["rm", "-r", dir_path])
            assert result is None
            mock_print.assert_called_once_with('Удаление отменено.')
            mock_log.assert_called_once_with("rm -r test_dir", success=False, error='Удаление отменено пользователем')

    def test_rm_no_path_specified(self):
        with patch('builtins.print') as mock_print, \
             patch('src.rm.log') as mock_log:
            result = self.rm(["rm"])
            assert result is None
            mock_print.assert_called_once_with("Ошибка: не указан путь для удаления")
            mock_log.assert_called_once_with("rm", success=False, error="No path specified")

    def test_rm_no_directory_specified_with_r(self):
        with patch('builtins.print') as mock_print, \
             patch('src.rm.log') as mock_log:
            result = self.rm(["rm", "-r"])
            assert result is None
            mock_print.assert_called_once_with("Ошибка: не указан каталог для рекурсивного удаления")
            mock_log.assert_called_once()

    def test_rm_protected_path(self):
        with patch('builtins.print') as mock_print, \
             patch('src.rm.log') as mock_log:
            result = self.rm(["rm", "/"])
            assert result is None
            mock_print.assert_called_once()
            assert "Ошибка" in mock_print.call_args[0][0]
            mock_log.assert_called_once()

    def test_rm_file_not_found(self):
        file_path = "nonexistent.txt"
        with patch('os.path.exists', return_value=False), \
             patch('builtins.print') as mock_print, \
             patch('src.rm.log') as mock_log:
            result = self.rm(["rm", file_path])
            assert result is None
            assert mock_print.call_count == 1
            assert "Ошибка" in mock_print.call_args[0][0]
            mock_log.assert_called_once()

