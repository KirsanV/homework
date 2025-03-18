import json
from typing import Any, Dict, List

from src.external_api import convert_to_rub


def load_transactions(filename: str) -> List[Dict[str, Any]]:
    """
    Загрущк транзакции из указанного файла в формате JSON
    и ловля ошибок по чтению JSON и местоположению
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def main(transactions: List[Dict[str, Any]]) -> None:
    """
    Основная функция, загружающая транзакции и конвертирующая суммы в рубли.
    """
#    transactions: List[Dict[str, Any]] = load_transactions('operations.json')
    for transaction in transactions:
        try:
            print("Available keys in transaction:", transaction.keys())
            if 'operationAmount' in transaction and 'amount' in transaction['operationAmount']:
                amount_in_rub = convert_to_rub(transaction)
                print(f"Transaction ID: {transaction['id']}, Amount in RUB: {amount_in_rub:.2f}")
            else:
                print(
                    f"Transaction ID: {transaction.get('id', 'unknown')} does not contain"
                    f" 'operationAmount' or 'amount' information.")

        except Exception as e:
            print(f"Failed to process transaction ID: {transaction.get('id', 'unknown')}. Error: {e}")
