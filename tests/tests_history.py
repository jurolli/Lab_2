from unittest.mock import Mock, patch, mock_open
from pathlib import Path
from src.history import show_history, hist_history
import pytest

class TestHistory:
    def setup_method(self):
        self.show_history = show_history
        self.hist_history = hist_history
        self.cwd = Path("/test/cwd")
        self.env = {}

    def test_show_history(self):
        history_content = "[2024-01-01 12:00:00] [1.] ls\n[2024-01-01 12:01:00] [2.] cd /test\n"
        
        with patch('builtins.open', mock_open(read_data=history_content)), \
             patch('builtins.print') as mock_print:
            result = self.show_history(["history", "2"])
            assert result is None
            assert mock_print.call_count == 2

    def test_show_history_empty(self):
        with patch('builtins.open', side_effect=FileNotFoundError()), \
             patch('builtins.print') as mock_print:
            result = self.show_history(["history", "5"])
            assert result is None
            mock_print.assert_called_once_with("История пуста или параметр n некорректен")

    def test_show_history_invalid_n(self):
        with patch('builtins.open', mock_open(read_data="")), \
             patch('builtins.print') as mock_print:
            result = self.show_history(["history", "invalid"])
            assert result is None
            mock_print.assert_called_once_with("История пуста или параметр n некорректен")

    def test_hist_history(self):
        with patch('builtins.open', mock_open()) as mock_file, \
             patch('src.history.datetime') as mock_datetime:
            mock_datetime.now.return_value.strftime.return_value = "[2024-01-01 12:00:00]"
            result = self.hist_history(1, ["ls", "-l"])
            assert result is None
            mock_file.assert_called()
            # Проверяем, что файл был открыт для записи
            assert any('a' in str(call) for call in mock_file.call_args_list)

