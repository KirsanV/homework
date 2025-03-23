import unittest
from typing import Any
from unittest.mock import patch

from src.external_api import convert_to_rub


class TestConvertToRub(unittest.TestCase):
    """
    Тестовый класс для проверки функции конвертации валют.
    """

    @patch('requests.get')  # Патчинг метода requests.get
    def test_convert_to_rub_success(self, mock_get: Any) -> None:
        """
        Тест успешной конвертации валюты в рубли.
        """

        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {"rates": {"RUB": 75.0}}

        transaction = {
            'operationAmount': {
                'amount': '100',
                'currency': {
                    'code': 'USD'
                }
            }
        }

        result = convert_to_rub(transaction)
        self.assertEqual(result, 7500.0)  # 100 USD * 75 RUB/USD = 7500 RUB

    @patch('requests.get')  # Патчинг метода requests.get
    def test_convert_to_rub_failure(self, mock_get: Any) -> None:
        """
        Тест неудачного обращения к API при конвертации валюты.
        """
        mock_response = mock_get.return_value
        mock_response.status_code = 404  # Устанавливаем фейковый статус-код 404
        mock_response.json.return_value = {"error": "Not Found"}

        transaction = {
            'operationAmount': {
                'amount': '100',
                'currency': {
                    'code': 'USD'
                }
            }
        }

        with self.assertRaises(Exception) as context:
            convert_to_rub(transaction)

        self.assertEqual(str(context.exception), "Error fetching exchange rates: 404")

    @patch('requests.get')  # Патчинг метода requests.get
    def test_convert_to_rub_invalid_data(self, mock_get: Any) -> None:
        """
        Тест обработки некорректных данных, возвращаемых API.

        :param mock_get: Мок-объект, который эмулирует поведение requests.get.
        """
        # Настраиваем мок-ответ
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {}  # Не возвращаем поле "rates"

        transaction = {
            'operationAmount': {
                'amount': '100',
                'currency': {
                    'code': 'USD'
                }
            }
        }

        with self.assertRaises(KeyError) as context:
            convert_to_rub(transaction)

        self.assertEqual(str(context.exception), "'rates'")  # Проверяем сообщение об ошибке


if __name__ == '__main__':
    unittest.main()
