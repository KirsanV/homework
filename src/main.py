import csv
import json
import os
from typing import Any, Dict, List

from src.masks import get_mask_account, get_mask_card_number
from src.transaction_finder import count_transactions_by_category, filter_transactions_by_description


def load_json(file_path: str):
    """Загружает данные из JSON файла."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_csv(file_path: str):
    """Загружает данные из CSV файла."""
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        return [row for row in reader]


def load_excel(file_path: str):
    """Загружает данные из Excel файла."""
    import pandas as pd
    return pd.read_excel(file_path).to_dict(orient='records')


def normalize_transaction(transaction: Dict[str, Any]) -> Dict[str, Any]:
    """Приводит транзакцию к единому формату."""
    if 'operationAmount' in transaction:
        # Формат для JSON
        return {
            'date': transaction['date'],
            'description': transaction['description'],
            'amount': transaction['operationAmount']['amount'],
            'currency_code': transaction['operationAmount']['currency']['code'],
            'state': transaction.get('state', ''),
            'from': transaction.get('from', ''),
            'to': transaction.get('to', '')
        }
    else:
        # Формат для цсв и эксель
        return {
            'date': transaction['date'],
            'description': transaction['description'],
            'amount': transaction['amount'],
            'currency_code': transaction['currency_code'],
            'state': transaction.get('state', ''),
            'from': transaction.get('from', ''),
            'to': transaction.get('to', '')
        }


def format_transaction(transaction: Dict[str, Any]) -> str:
    """Форматирует транзакцию для вывода."""
    date = transaction['date'][:10]  # Берем только дату
    description = transaction['description']
    amount = transaction['amount']
    currency_code = transaction['currency_code']

    # Маскировка номера карт и счетов
    from_info = transaction['from']
    to_info = transaction['to']

    if from_info:
        from_info = from_info.replace('Счет', 'Счет')
        from_info = get_mask_account(from_info) if 'Счет' in from_info else get_mask_card_number(from_info)

    if to_info:
        to_info = to_info.replace('Счет', 'Счет')
        to_info = get_mask_account(to_info) if 'Счет' in to_info else get_mask_card_number(to_info)

    output = f"{date} {description}\n"
    if from_info and to_info:
        output += f"{from_info} -> {to_info}\n"
    output += f"Сумма: {amount} {currency_code}\n"

    return output


def get_file_path(file_name: str) -> str:
    """Возвращает полный путь к файлу в зависимости от его имени."""
    base_dir = os.path.dirname(__file__)
    return os.path.join(base_dir, '..', file_name)


def main() -> None:
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("Пользователь: ")
    transactions = []

    if choice == '1':
        json_path = get_file_path('data/operations.json')
        transactions = load_json(json_path)
        print("Для обработки выбран JSON-файл.")
    elif choice == '2':
        csv_path = get_file_path('excel_cvv/transactions.csv')
        transactions = load_csv(csv_path)
        print("Для обработки выбран CSV-файл.")
    elif choice == '3':
        excel_path = get_file_path('excel_cvv/transactions_excel.xlsx')
        transactions = load_excel(excel_path)
        print("Для обработки выбран XLSX-файл.")
    else:
        print("Неверный выбор.")
        return

    # т.к. цсв и json имеют разную структуру пришлось приводить их к единому формату(иной путь я не нашел)
    normalized_transactions: List[Dict[str, Any]] = [normalize_transaction(t) for t in transactions]

    status_options: List[str] = ['EXECUTED', 'CANCELED', 'PENDING']
    while True:
        status: str = input(
            "Введите статус, по которому необходимо выполнить фильтрацию."
            " Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\nПользователь: ")
        if status.upper() in status_options:
            print(f"Операции отфильтрованы по статусу \"{status.upper()}\"")
            filtered_transactions = [t for t in normalized_transactions if
                                     isinstance(t.get('state'), str) and t['state'].upper() == status.upper()]
            break
        else:
            print(f"Статус операции \"{status}\" недоступен.")

    # Дополнительные фильтры
    sort_by_date: bool = input("Отсортировать операции по дате? Да/Нет\nПользователь: ").strip().lower() == 'да'
    if sort_by_date:
        order: str = input("Отсортировать по возрастанию или по убыванию?\nПользователь: ").strip().lower()
        if order == 'по возрастанию':
            filtered_transactions.sort(key=lambda x: x['date'])
        elif order == 'по убыванию':
            filtered_transactions.sort(key=lambda x: x['date'], reverse=True)

    only_rub: bool = input("Выводить только рублевые транзакции? Да/Нет\nПользователь: ").strip().lower() == 'да'
    if only_rub:
        filtered_transactions = [t for t in filtered_transactions if t['currency_code'] == 'RUB']

    filter_description: bool = input(
        "Отфильтровать список транзакций по определенному слову в описании?"
        " Да/Нет\nПользователь: ").strip().lower() == 'да'
    if filter_description:
        search_string: str = input("Введите слово для фильтрации по описанию:\nПользователь: ")
        filtered_transactions = filter_transactions_by_description(filtered_transactions, search_string)

    # Подсчет транзакций по категориям
    categories: List[str] = [
        'Перевод организации',
        'Открытие вклада',
        'Перевод со счета на счет',
        'Перевод с карты на карту'
    ]
    category_counts: Dict[str, int] = count_transactions_by_category(filtered_transactions, categories)

    # Вывод результатов
    if filtered_transactions:
        print("Распечатываю итоговый список транзакций...")
        print(f"Всего банковских операций в выборке: {len(filtered_transactions)}")
        for transaction in filtered_transactions:
            print(format_transaction(transaction))  # Используем новую функцию для форматирования

        # Выводим подсчет по категориям
        print("\nПодсчет транзакций по категориям:")
        for category, count in category_counts.items():
            print(f"{category}: {count}")
    else:
        print("Не найдено ни одной транзакции, подходящей под условия фильтрации.")
