import re
from collections import Counter
from typing import Dict, List


def filter_transactions_by_description(transactions: List[Dict], search_string: str) -> List[Dict]:
    """
        Фильтрует список транзакций по описанию, возвращая только те транзакции,
        которые содержат искомую строку поиска.
        """
    pattern = re.compile(re.escape(search_string), re.IGNORECASE)
    return [transaction for transaction in transactions if pattern.search(transaction.get('description', ''))]


def count_transactions_by_category(transactions: List[Dict], categories: List[str]) -> Dict[str, int]:
    """Подсчитывает количество транзакций по категориям, используя Counter."""
    category_count = Counter()

    for transaction in transactions:
        description = transaction.get('description', '')
        for category in categories:
            if category in description:
                category_count[category] += 1

    return dict(category_count)
