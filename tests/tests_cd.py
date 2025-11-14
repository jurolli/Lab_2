from unittest.mock import Mock, patch
from pathlib import Path
from src.cd import cd
import pytest

class TestCd:
    def setup_method(self):
        self.cd = cd
        self.cwd = Path("/test/cwd")
        self.env = {}

    def test_cd_with_path(self):
        test_path = "/test/directory"
        with patch('os.path.expanduser', return_value=test_path), \
             patch('os.chdir') as mock_chdir, \
             patch('os.getcwd', return_value=test_path), \
             patch('builtins.print') as mock_print, \
             patch('src.cd.log') as mock_log:
            result = self.cd(["cd", test_path])
            assert result is None
            mock_chdir.assert_called_once_with(test_path)
            mock_print.assert_called_once()
            mock_log.assert_called_once_with("cd /test/directory", success=True)

    def test_cd_home_directory(self):
        home_path = "/home/user"
        with patch('os.path.expanduser', return_value=home_path), \
             patch('os.chdir') as mock_chdir, \
             patch('os.getcwd', return_value=home_path), \
             patch('builtins.print') as mock_print, \
             patch('src.cd.log') as mock_log:
            result = self.cd(["cd"])
            assert result is None
            mock_chdir.assert_called_once_with(home_path)
            mock_log.assert_called_once_with("cd", success=True)

    def test_cd_tilde(self):
        home_path = "/home/user"
        with patch('os.path.expanduser', return_value=home_path), \
             patch('os.chdir') as mock_chdir, \
             patch('os.getcwd', return_value=home_path), \
             patch('builtins.print') as mock_print, \
             patch('src.cd.log') as mock_log:
            result = self.cd(["cd", "~"])
            assert result is None
            mock_chdir.assert_called_once_with(home_path)
            mock_log.assert_called_once_with("cd ~", success=True)

    def test_cd_parent_directory(self):
        parent_path = "/test"
        current_path = "/test/cwd"
        with patch('os.getcwd', return_value=current_path), \
             patch('os.path.abspath', return_value=parent_path), \
             patch('os.path.join', return_value=parent_path), \
             patch('os.chdir') as mock_chdir, \
             patch('builtins.print') as mock_print, \
             patch('src.cd.log') as mock_log:
            result = self.cd(["cd", ".."])
            assert result is None
            mock_chdir.assert_called_once()
            mock_log.assert_called_once_with("cd ..", success=True)

    def test_cd_error(self):
        test_path = "/nonexistent"
        with patch('os.path.expanduser', return_value=test_path), \
             patch('os.chdir', side_effect=FileNotFoundError("No such directory")), \
             patch('builtins.print') as mock_print, \
             patch('src.cd.log') as mock_log:
            result = self.cd(["cd", test_path])
            assert result is None
            assert mock_print.call_count == 1
            assert "Ошибка" in mock_print.call_args[0][0]
            mock_log.assert_called_once()

