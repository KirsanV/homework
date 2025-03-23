from typing import Dict, List

import pandas as pd


def read_transactions_from_csv(file_path: str) -> List[Dict]:
    """Считывает финансовые операции из CSV файла и возвращает список словарей."""
    try:
        df = pd.read_csv(file_path, sep=';', encoding='utf-8')
        # DF в список словарей
        transactions = df.to_dict(orient='records')
        return transactions
    except Exception as e:
        print(f"Ошибка при чтении CSV файла: {e}")
        return []


def read_transactions_from_excel(file_path: str) -> List[Dict]:
    """Считывает финансовые операции из Excel файла и возвращает список словарей."""
    try:
        df = pd.read_excel(file_path)
        # DF в список словарей
        transactions = df.to_dict(orient='records')
        return transactions
    except Exception as e:
        print(f"Ошибка при чтении Excel файла: {e}")
        return []

# Функция для теста работоспособности кода вот
# def testim_code():
#     csv_file_path = '../excel_cvv/transactions.csv'
#     excel_file_path = '../excel_cvv/transactions_excel.xlsx'
#     csv_transactions = read_transactions_from_csv(csv_file_path)
#     excel_transactions = read_transactions_from_excel(excel_file_path)
#     print("Транзакции csv:")
#     print(csv_transactions)
#     print("\nТранзакции exel:")
#     print(excel_transactions)
# if __name__ == "__main__":
#     testim_code()
