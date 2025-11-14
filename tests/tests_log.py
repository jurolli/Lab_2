from unittest.mock import Mock, patch, mock_open
from pathlib import Path
from src.log import log
import pytest

class TestLog:
    def setup_method(self):
        self.log = log
        self.cwd = Path("/test/cwd")
        self.env = {}

    def test_log_success(self):
        command = "ls -l"
        with patch('builtins.open', mock_open()) as mock_file, \
             patch('src.log.datetime') as mock_datetime:
            mock_datetime.now.return_value.strftime.return_value = "[2024-01-01 12:00:00]"
            result = self.log(command, success=True)
            assert result is None
            mock_file.assert_called()
            # Проверяем, что файл был открыт для записи
            handle = mock_file()
            handle.write.assert_called()

    def test_log_error(self):
        command = "cat nonexistent.txt"
        error = "File not found"
        with patch('builtins.open', mock_open()) as mock_file, \
             patch('src.log.datetime') as mock_datetime:
            mock_datetime.now.return_value.strftime.return_value = "[2024-01-01 12:00:00]"
            result = self.log(command, success=False, error=error)
            assert result is None
            mock_file.assert_called()
            handle = mock_file()
            handle.write.assert_called()
            # Проверяем, что в запись включена ошибка
            write_call = handle.write.call_args[0][0]
            assert "ERROR" in write_call
            assert error in write_call

