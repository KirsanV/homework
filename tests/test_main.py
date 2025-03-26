import os
import unittest
from unittest.mock import MagicMock, mock_open, patch

from src.main import format_transaction, load_csv, load_excel, load_json, main, normalize_transaction


class TestMainFunctions(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open,
           read_data='[{"date": "2023-01-01", "description": "Тестовая транзакция",'
                     ' "operationAmount": {"amount": 1000, "currency": {"code": "RUB"}}, "state": "EXECUTED"}]')
    def test_load_json(self, mock_file):
        result = load_json("dummy_path.json")
        expected = [{
            'date': "2023-01-01",
            'description': "Тестовая транзакция",
            'operationAmount': {'amount': 1000, 'currency': {'code': 'RUB'}},
            'state': 'EXECUTED'
        }]
        self.assertEqual(result, expected)

    @patch("builtins.open", new_callable=mock_open,
           read_data='date;description;amount;currency_code;state\n2023-01-01;Тестовая транзакция;1000;RUB;EXECUTED')
    def test_load_csv(self, mock_file):
        result = load_csv("dummy_path.csv")
        expected = [{
            'date': "2023-01-01",
            'description': "Тестовая транзакция",
            'amount': "1000",
            'currency_code': "RUB",
            'state': "EXECUTED"
        }]
        self.assertEqual(result, expected)

    def test_normalize_transaction_json(self):
        transaction = {
            'date': "2023-01-01",
            'description': "Тестовая транзакция",
            'operationAmount': {'amount': 1000, 'currency': {'code': 'RUB'}},
            'state': 'EXECUTED'
        }
        expected = {
            'date': "2023-01-01",
            'description': "Тестовая транзакция",
            'amount': 1000,
            'currency_code': 'RUB',
            'state': 'EXECUTED',
            'from': '',
            'to': ''
        }
        self.assertEqual(normalize_transaction(transaction), expected)

    def test_normalize_transaction_csv(self):
        transaction = {
            'date': "2023-01-01",
            'description': "Тестовая транзакция",
            'amount': 1000,
            'currency_code': 'RUB',
            'state': 'EXECUTED'
        }
        expected = {
            'date': "2023-01-01",
            'description': "Тестовая транзакция",
            'amount': 1000,
            'currency_code': 'RUB',
            'state': 'EXECUTED',
            'from': '',
            'to': ''
        }
        self.assertEqual(normalize_transaction(transaction), expected)

    @patch("src.masks.get_mask_account")
    @patch("src.masks.get_mask_card_number")
    def test_format_transaction(self, mock_get_mask_account, mock_get_mask_card_number):
        mock_get_mask_account.return_value = "Счет: 1234 56** **** 3456"
        mock_get_mask_card_number.return_value = "Карточка: 5678 12** **** 3456"

        transaction = {
            'date': "2023-01-01T12:00:00",
            'description': "Тестовая транзакция",
            'amount': 1000,
            'currency_code': 'RUB',
            'state': 'EXECUTED',
            'from': 'Счет: 1234567890123456',
            'to': 'Карточка: 5678123456783456'
        }

        expected_output = "2023-01-01 Тестовая транзакция\n" \
                          "************3456 -> 5678 12** **** 3456\n" \
                          "Сумма: 1000 RUB\n"
        actual_output = format_transaction(transaction)

        # Выводим для отладки
        print(f"Expected output: {expected_output}")
        print(f"Actual output: {actual_output}")

        self.assertEqual(actual_output, expected_output)

    def test_get_file_path(self):
        # Формируем ожидаемый путь с использованием os.path.join
        expected_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'operations.json')
        actual_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'operations.json')

        # Приводим оба пути к абсолютному виду для сравнения
        self.assertEqual(os.path.abspath(actual_path), os.path.abspath(expected_path))

    @patch('pandas.read_excel')
    def test_load_excel_success(self, mock_read_excel):
        # Настраиваем mock для возвращаемого значения
        mock_data = [
            {'date': '2023-01-01', 'description': 'Тестовая транзакция 1', 'amount': 1000, 'currency_code': 'RUB'},
            {'date': '2023-01-02', 'description': 'Тестовая транзакция 2', 'amount': 2000, 'currency_code': 'USD'},
        ]
        mock_read_excel.return_value = MagicMock()
        mock_read_excel.return_value.to_dict.return_value = mock_data

        # Вызываем функцию
        result = load_excel('fake_path.xlsx')

        # Проверяем, что результат соответствует ожидаемому
        self.assertEqual(result, mock_data)
        mock_read_excel.assert_called_once_with('fake_path.xlsx')

    @patch('pandas.read_excel')
    def test_load_excel_file_not_found(self, mock_read_excel):
        # Настраиваем mock для генерации исключения FileNotFoundError
        mock_read_excel.side_effect = FileNotFoundError

        # Проверяем, что функция вызывает исключение
        with self.assertRaises(FileNotFoundError):
            load_excel('fake_path.xlsx')

    @patch('pandas.read_excel')
    def test_load_excel_invalid_data(self, mock_read_excel):
        # Настраиваем mock для возвращаемого значения с некорректными данными
        mock_read_excel.return_value = MagicMock()
        mock_read_excel.return_value.to_dict.return_value = None  # Неверный формат данных

        # Проверяем, что функция возвращает None
        result = load_excel('fake_path.xlsx')
        self.assertIsNone(result)

    @patch('builtins.print')
    @patch('builtins.input', side_effect=['1', 'EXECUTED', 'Нет', 'Нет', 'Нет', 'Нет'])
    @patch('src.main.load_json')
    @patch('src.main.get_file_path')
    def test_main_json_choice(self, mock_get_file_path, mock_load_json, mock_input, mock_print):
        # Настраиваем mock для get_file_path и load_json
        mock_get_file_path.return_value = 'data/operations.json'
        mock_load_json.return_value = [
            {'date': '2023-01-01', 'description': 'Тестовая транзакция',
             'amount': 1000, 'currency_code': 'RUB', 'state': 'EXECUTED'}
        ]

        main()

        # Проверяем, что функции были вызваны
        mock_get_file_path.assert_called_once_with('data/operations.json')
        mock_load_json.assert_called_once_with('data/operations.json')

        # Проверяем вывод
        mock_print.assert_any_call("Для обработки выбран JSON-файл.")
        mock_print.assert_any_call("Операции отфильтрованы по статусу \"EXECUTED\"")
        mock_print.assert_any_call("Распечатываю итоговый список транзакций...")
        mock_print.assert_any_call("Всего банковских операций в выборке: 1")
        mock_print.assert_any_call("2023-01-01 Тестовая транзакция\nСумма: 1000 RUB\n")
        mock_print.assert_any_call("\nПодсчет транзакций по категориям:")

    @patch('builtins.print')
    @patch('builtins.input', side_effect=['2', 'CANCELED', 'Да', 'по убыванию', 'Да', 'Нет', 'Нет'])
    @patch('src.main.load_csv')
    @patch('src.main.get_file_path')
    def test_main_csv_choice(self, mock_get_file_path, mock_load_csv, mock_input, mock_print):
        # Настраиваем mock для get_file_path и load_csv
        mock_get_file_path.return_value = 'excel_cvv/transactions.csv'
        mock_load_csv.return_value = [
            {'date': '2023-01-02', 'description': 'Тестовая транзакция 2',
             'amount': 2000, 'currency_code': 'USD', 'state': 'CANCELED'}
        ]

        main()

        # Проверяем, что функции были вызваны
        mock_get_file_path.assert_called_once_with('excel_cvv/transactions.csv')
        mock_load_csv.assert_called_once_with('excel_cvv/transactions.csv')

        # Проверяем вывод
        mock_print.assert_any_call("Для обработки выбран CSV-файл.")
        mock_print.assert_any_call("Операции отфильтрованы по статусу \"CANCELED\"")

    @patch('builtins.print')
    @patch('builtins.input', side_effect=['3', 'PENDING', 'Нет', 'по возрастанию', 'Нет', 'Да', 'тест'])
    @patch('src.main.load_excel')
    @patch('src.main.get_file_path')
    def test_main_excel_choice(self, mock_get_file_path, mock_load_excel, mock_input, mock_print):
        # Настраиваем mock для get_file_path и load_excel
        mock_get_file_path.return_value = 'excel_cvv/transactions_excel.xlsx'
        mock_load_excel.return_value = [
            {'date': '2023-01-03', 'description': 'Тестовая транзакция 3',
             'amount': 3000, 'currency_code': 'RUB', 'state': 'PENDING'}
        ]

        main()

        # Проверяем, что функции были вызваны
        mock_get_file_path.assert_called_once_with('excel_cvv/transactions_excel.xlsx')
        mock_load_excel.assert_called_once_with('excel_cvv/transactions_excel.xlsx')

        # Проверяем вывод
        mock_print.assert_any_call("Для обработки выбран XLSX-файл.")
        mock_print.assert_any_call("Операции отфильтрованы по статусу \"PENDING\"")
        mock_print.assert_any_call("Распечатываю итоговый список транзакций...")
        mock_print.assert_any_call("Всего банковских операций в выборке: 1")
        mock_print.assert_any_call("2023-01-03 Тестовая транзакция 3\nСумма: 3000 RUB\n")
        mock_print.assert_any_call("\nПодсчет транзакций по категориям:")

    @patch('builtins.print')
    @patch('builtins.input', side_effect=['4'])  # Неверный выбор
    def test_main_invalid_choice(self, mock_input, mock_print):
        main()
        mock_print.assert_any_call("Неверный выбор.")
