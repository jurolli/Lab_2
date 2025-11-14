from unittest.mock import Mock, patch, mock_open
from pathlib import Path
from src.undo import undo
import pytest

class TestUndo:
    def setup_method(self):
        self.undo = undo
        self.cwd = Path("/test/cwd")
        self.env = {}

    def test_undo_cp_file(self):
        log_content = "[2024-01-01 12:00:00] cp source.txt dest.txt\n"
        with patch('builtins.open', mock_open(read_data=log_content)), \
             patch('src.undo.os.path.isdir', return_value=False), \
             patch('src.undo.os.path.isfile', return_value=True), \
             patch('src.undo.os.remove') as mock_remove, \
             patch('builtins.print') as mock_print:
            result = self.undo()
            assert result is None
            mock_remove.assert_called_once_with("dest.txt")
            mock_print.assert_called_once()

    def test_undo_cp_directory(self):
        log_content = "[2024-01-01 12:00:00] cp source_dir dest_dir\n"
        with patch('builtins.open', mock_open(read_data=log_content)), \
             patch('os.path.isdir', return_value=True), \
             patch('shutil.rmtree') as mock_rmtree, \
             patch('builtins.print') as mock_print:
            result = self.undo()
            assert result is None
            mock_rmtree.assert_called_once_with("dest_dir")
            mock_print.assert_called_once()

    def test_undo_mv(self):
        log_content = "[2024-01-01 12:00:00] mv source.txt dest.txt\n"
        with patch('builtins.open', mock_open(read_data=log_content)), \
             patch('os.path.exists', return_value=True), \
             patch('shutil.move') as mock_move, \
             patch('builtins.print') as mock_print:
            result = self.undo()
            assert result is None
            mock_move.assert_called_once_with("dest.txt", "source.txt")
            mock_print.assert_called_once()

    def test_undo_rm(self):
        log_content = "[2024-01-01 12:00:00] rm test.txt\n"
        with patch('builtins.open', mock_open(read_data=log_content)), \
             patch('os.path.exists', return_value=True), \
             patch('os.path.basename', return_value="test.txt"), \
             patch('os.path.join', return_value=".trash/test.txt"), \
             patch('shutil.move') as mock_move, \
             patch('builtins.print') as mock_print:
            result = self.undo()
            assert result is None
            mock_move.assert_called_once()
            mock_print.assert_called_once()

    def test_undo_empty_log(self):
        with patch('builtins.open', mock_open(read_data="")), \
             patch('builtins.print') as mock_print:
            result = self.undo()
            assert result is None
            mock_print.assert_called_once_with("Нет операций для отмены")

    def test_undo_file_not_found(self):
        with patch('builtins.open', side_effect=FileNotFoundError()), \
             patch('builtins.print') as mock_print:
            result = self.undo()
            assert result is None
            mock_print.assert_called_once_with("Лог операций пуст")

    def test_undo_cp_object_not_found(self):
        log_content = "[2024-01-01 12:00:00] cp source.txt dest.txt\n"
        with patch('builtins.open', mock_open(read_data=log_content)), \
             patch('os.path.isfile', return_value=False), \
             patch('os.path.isdir', return_value=False), \
             patch('builtins.print') as mock_print:
            result = self.undo()
            assert result is None
            mock_print.assert_called_once_with("Ошибка: объект для удаления не найден")

    def test_undo_mv_object_not_found(self):
        log_content = "[2024-01-01 12:00:00] mv source.txt dest.txt\n"
        with patch('builtins.open', mock_open(read_data=log_content)), \
             patch('os.path.exists', return_value=False), \
             patch('builtins.print') as mock_print:
            result = self.undo()
            assert result is None
            mock_print.assert_called_once_with("Ошибка: объект для возврата не найден")

    def test_undo_rm_object_not_found(self):
        log_content = "[2024-01-01 12:00:00] rm test.txt\n"
        with patch('builtins.open', mock_open(read_data=log_content)), \
             patch('os.path.exists', return_value=False), \
             patch('builtins.print') as mock_print:
            result = self.undo()
            assert result is None
            mock_print.assert_called_once_with("Ошибка: объект не найден в .trash")

