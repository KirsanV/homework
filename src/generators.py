from typing import Dict, Generator, List


def filter_by_currency(transactions: List[Dict], currency: str) -> Generator[Dict, None, None]:
    """Генератор для фильтрации транзакций по указанной валюте."""
    for transaction in transactions:
        if transaction.get("operationAmount", {}).get("currency", {}).get("code") == currency:
            yield transaction


def transaction_descriptions(transactions: List[Dict]) -> Generator[str, None, None]:
    """Генератор для выдачи описания каждой транзакции."""
    for transaction in transactions:
        yield transaction.get("description", "")


def card_number_generator(start: int, end: int) -> Generator[str, None, None]:
    """Генератор для выдачи номеров банковских карт."""
    for number in range(start, end + 1):
        yield (f"{number:016d}"[:4] + " " + f"{number:016d}"[4:8] + " " +
               f"{number:016d}"[8:12] + " " + f"{number:016d}"[12:16])
