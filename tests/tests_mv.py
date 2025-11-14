from unittest.mock import Mock, patch
from pathlib import Path
from src.mv import mv
import pytest

class TestMv:
    def setup_method(self):
        self.mv = mv
        self.cwd = Path("/test/cwd")
        self.env = {}

    def test_mv_file(self):
        source = "source.txt"
        dest = "dest.txt"
        with patch('os.path.exists', return_value=True), \
             patch('os.path.isdir', return_value=False), \
             patch('shutil.move') as mock_move, \
             patch('builtins.print') as mock_print, \
             patch('src.mv.log') as mock_log:
            result = self.mv(["mv", source, dest])
            assert result is None
            mock_move.assert_called_once_with(source, dest)
            mock_print.assert_called_once()
            mock_log.assert_called_once_with("mv source.txt dest.txt", success=True)

    def test_mv_to_directory(self):
        source = "source.txt"
        dest_dir = "/test/dir"
        expected_dest = f"{dest_dir}/source.txt"
        with patch('os.path.exists', return_value=True), \
             patch('os.path.isdir', side_effect=lambda x: x == dest_dir), \
             patch('os.path.basename', return_value="source.txt"), \
             patch('os.path.join', return_value=expected_dest), \
             patch('shutil.move') as mock_move, \
             patch('builtins.print') as mock_print, \
             patch('src.mv.log') as mock_log:
            result = self.mv(["mv", source, dest_dir])
            assert result is None
            mock_move.assert_called_once()
            mock_log.assert_called_once_with("mv source.txt /test/dir", success=True)

    def test_mv_not_enough_arguments(self):
        with patch('builtins.print') as mock_print, \
             patch('src.mv.log') as mock_log:
            result = self.mv(["mv"])
            assert result is None
            mock_print.assert_called_once_with("Ошибка: недостаточно аргументов для перемещения")
            mock_log.assert_called_once_with("mv", success=False, error="Not enough arguments")

    def test_mv_source_not_found(self):
        source = "nonexistent.txt"
        dest = "dest.txt"
        with patch('os.path.exists', return_value=False), \
             patch('builtins.print') as mock_print, \
             patch('src.mv.log') as mock_log:
            result = self.mv(["mv", source, dest])
            assert result is None
            assert mock_print.call_count == 1
            assert "Ошибка" in mock_print.call_args[0][0]
            mock_log.assert_called_once()

