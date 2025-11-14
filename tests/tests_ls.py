from unittest.mock import Mock, patch
from pathlib import Path
from src.ls import ls
import pytest

class TestLs:
    def setup_method(self):
        self.ls = ls
        self.cwd = Path("/test/cwd")
        self.env = {}

    def test_ls_current_directory(self):
        entries = ["file1.txt", "file2.txt", "dir1"]
        with patch('os.listdir', return_value=entries), \
             patch('builtins.print') as mock_print, \
             patch('src.ls.log') as mock_log:
            result = self.ls(["ls"])
            assert result is None
            assert mock_print.call_count == len(entries)
            mock_log.assert_called_once_with("ls", success=True)

    def test_ls_with_path(self):
        test_path = "/test/dir"
        entries = ["file1.txt", "file2.txt"]
        with patch('os.listdir', return_value=entries), \
             patch('builtins.print') as mock_print, \
             patch('src.ls.log') as mock_log:
            result = self.ls(["ls", test_path])
            assert result is None
            assert mock_print.call_count == len(entries)
            mock_log.assert_called_once_with(f"ls {test_path}", success=True)

    def test_ls_with_l_flag(self):
        entries = ["file1.txt"]
        mock_stat = Mock()
        mock_stat.st_mode = 33188  # обычный файл
        mock_stat.st_size = 1024
        mock_stat.st_mtime = 1609459200  # 2021-01-01 00:00:00
        
        with patch('os.listdir', return_value=entries), \
             patch('os.path.join', return_value="file1.txt"), \
             patch('os.stat', return_value=mock_stat), \
             patch('stat.filemode', return_value="-rw-r--r--"), \
             patch('time.strftime', return_value="2021-01-01 00:00:00"), \
             patch('time.localtime', return_value=None), \
             patch('builtins.print') as mock_print, \
             patch('src.ls.log') as mock_log:
            result = self.ls(["ls", "-l"])
            assert result is None
            assert mock_print.call_count == len(entries)
            mock_log.assert_called_once_with("ls -l", success=True)

    def test_ls_with_l_flag_and_path(self):
        test_path = "/test/dir"
        entries = ["file1.txt"]
        mock_stat = Mock()
        mock_stat.st_mode = 33188
        mock_stat.st_size = 1024
        mock_stat.st_mtime = 1609459200
        
        with patch('os.listdir', return_value=entries), \
             patch('os.path.join', return_value=f"{test_path}/file1.txt"), \
             patch('os.stat', return_value=mock_stat), \
             patch('stat.filemode', return_value="-rw-r--r--"), \
             patch('time.strftime', return_value="2021-01-01 00:00:00"), \
             patch('time.localtime', return_value=None), \
             patch('builtins.print') as mock_print, \
             patch('src.ls.log') as mock_log:
            result = self.ls(["ls", "-l", test_path])
            assert result is None
            assert mock_print.call_count == len(entries)
            mock_log.assert_called_once_with(f"ls -l {test_path}", success=True)

    def test_ls_error(self):
        test_path = "/nonexistent"
        with patch('os.listdir', side_effect=FileNotFoundError("No such directory")), \
             patch('builtins.print') as mock_print, \
             patch('src.ls.log') as mock_log:
            result = self.ls(["ls", test_path])
            assert result is None
            assert mock_print.call_count == 1
            assert "Ошибка" in mock_print.call_args[0][0]
            mock_log.assert_called_once()

