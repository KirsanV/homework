import unittest
from unittest.mock import patch

import pandas as pd

from src.transaction_reader import read_transactions_from_csv, read_transactions_from_excel


class TestTransactionReader(unittest.TestCase):

    @patch('pandas.read_csv')
    def test_read_transactions_from_csv(self, mock_read_csv):
        mock_read_csv.return_value = pd.DataFrame({
            'date': ['2023-01-01', '2023-01-02'],
            'amount': [100, 200],
            'description': ['Test transaction 1', 'Test transaction 2']
        })

        transactions = read_transactions_from_csv('dummy_path.csv')

        # Проверка, что данные считываютс правильно
        self.assertEqual(len(transactions), 2)
        self.assertEqual(transactions[0]['amount'], 100)
        self.assertEqual(transactions[1]['description'], 'Test transaction 2')

        mock_read_csv.assert_called_once_with('dummy_path.csv', sep=';', encoding='utf-8')

    @patch('pandas.read_excel')
    def test_read_transactions_from_excel(self, mock_read_excel):
        # Настройка мока для ДФ
        mock_read_excel.return_value = pd.DataFrame({
            'date': ['2023-01-01', '2023-01-02'],
            'amount': [100, 200],
            'description': ['Test transaction 1', 'Test transaction 2']
        })

        transactions = read_transactions_from_excel('dummy_path.xlsx')

        # Проверка, что данные считываются правильно
        self.assertEqual(len(transactions), 2)
        self.assertEqual(transactions[0]['amount'], 100)
        self.assertEqual(transactions[1]['description'], 'Test transaction 2')

        mock_read_excel.assert_called_once_with('dummy_path.xlsx')
