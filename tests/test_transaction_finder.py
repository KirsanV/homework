import unittest

from src.transaction_finder import count_transactions_by_category, filter_transactions_by_description


class TestTransactionFunctions(unittest.TestCase):

    def setUp(self):
        """Создаем тестовые данные для использования в тестах."""
        self.transactions = [
            {'description': 'Оплата за интернет', 'amount': 100, 'currency_code': 'RUB'},
            {'description': 'Перевод на карту', 'amount': 200, 'currency_code': 'RUB'},
            {'description': 'Оплата за мобильную связь', 'amount': 150, 'currency_code': 'RUB'},
            {'description': 'Покупка в магазине', 'amount': 300, 'currency_code': 'RUB'},
            {'description': 'Оплата за коммунальные услуги', 'amount': 250, 'currency_code': 'RUB'},
        ]

    def test_filter_transactions_by_description(self):
        """Тестируем фильтрацию транзакций по описанию."""
        result = filter_transactions_by_description(self.transactions, 'оплата')
        expected = [
            {'description': 'Оплата за интернет', 'amount': 100, 'currency_code': 'RUB'},
            {'description': 'Оплата за мобильную связь', 'amount': 150, 'currency_code': 'RUB'},
            {'description': 'Оплата за коммунальные услуги', 'amount': 250, 'currency_code': 'RUB'},
        ]
        self.assertEqual(result, expected)

    def test_filter_transactions_by_description_no_match(self):
        """Тестируем фильтрацию, когда нет совпадений."""
        result = filter_transactions_by_description(self.transactions, 'покупка в кафе')
        expected = []
        self.assertEqual(result, expected)

    def test_count_transactions_by_category(self):
        """Тестируем подсчет транзакций по категориям."""
        categories = ['оплата', 'покупка']
        result = count_transactions_by_category(self.transactions, categories)
        expected = {}
        self.assertEqual(result, expected)

    def test_count_transactions_by_category_no_matches(self):
        """Тестируем подсчет, когда нет совпадений по категориям."""
        categories = ['покупка в кафе']
        result = count_transactions_by_category(self.transactions, categories)
        expected = {}
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
