import json
import unittest
from typing import Any, Dict, List
from unittest.mock import mock_open, patch

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

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps([
        {
            "id": 1,
            "operationAmount": {
                "amount": "100",
                "currency": {"code": "USD"}
            }
        },
        {
            "id": 2,
            "operationAmount": {
                "amount": "200",
                "currency": {"code": "EUR"}
            }
        }
    ]))
    @patch('src.utils.convert_to_rub', side_effect=[7500.0, 18000.0])  # Замените на имя вашего модуля
    def test_main_success(self, mock_convert_to_rub: Any, mock_open: Any) -> None:
        """
        Тестирование обработки успешных транзакций.
        """
        with patch('builtins.print') as mock_print:
            main()
            mock_open.assert_called_once_with('operations.json', 'r', encoding='utf-8')
            mock_print.assert_any_call("Transaction ID: 1, Amount in RUB: 7500.00")
            mock_print.assert_any_call("Transaction ID: 2, Amount in RUB: 18000.00")


if __name__ == "__main__":
    unittest.main()
