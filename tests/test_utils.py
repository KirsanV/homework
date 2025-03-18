import json
import unittest
from typing import Any, Dict, List
from unittest.mock import mock_open, patch, MagicMock

from src.utils import load_transactions, main


class TestUtils(unittest.TestCase):
    """
    Тесты для функций утилит, используемых в проекте.
    """

    @patch("builtins.open", new_callable=mock_open,
           read_data='[{"id": 1, "operationAmount": {"amount": "100", "currency": {"code": "USD"}}}]')
    def test_load_transactions(self, mock_file: mock_open) -> None:
        """
        Тестирует функцию load_transactions.
        Проверяет, что функция корректно загружает транзакции из файла
        и возвращает ожидаемую структуру данных.
        """
        transactions: List[Dict[str, Any]] = load_transactions('data/operations.json')
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0]["id"], 1)
        self.assertIn("operationAmount", transactions[0])

if __name__ == "__main__":
    unittest.main()
