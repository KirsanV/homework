# import json
# from typing import Any, Dict, List
#
# from src.external_api import convert_to_rub
#
#
# def load_transactions(filename: str) -> List[Dict[str, Any]]:
#     """
#     Загрущк транзакции из указанного файла в формате JSON
#     и ловля ошибок по чтению JSON и местоположению
#     """
#     try:
#         with open(filename, 'r', encoding='utf-8') as file:
#             return json.load(file)
#     except FileNotFoundError:
#         return []
#     except json.JSONDecodeError:
#         return []
#
#
# def main(transactions: List[Dict[str, Any]]) -> None:
#     """
#     Основная функция, загружающая транзакции и конвертирующая суммы в рубли.
#     """
# #    transactions: List[Dict[str, Any]] = load_transactions('operations.json')
#     for transaction in transactions:
#         try:
#             print("Available keys in transaction:", transaction.keys())
#             if 'operationAmount' in transaction and 'amount' in transaction['operationAmount']:
#                 amount_in_rub = convert_to_rub(transaction)
#                 print(f"Transaction ID: {transaction['id']}, Amount in RUB: {amount_in_rub:.2f}")
#             else:
#                 print(
#                     f"Transaction ID: {transaction.get('id', 'unknown')} does not contain"
#                     f" 'operationAmount' or 'amount' information.")
#
#         except Exception as e:
#             print(f"Failed to process transaction ID: {transaction.get('id', 'unknown')}. Error: {e}")

import json
import logging
import os
from typing import Any, Dict, List

from src.external_api import convert_to_rub

# Настройка логирования для модуля utils
log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Создаем логер
utils_logger = logging.getLogger('utils')
utils_logger.setLevel(logging.DEBUG)

# Создаем обработчик для записи логов в файл
utils_file_handler = logging.FileHandler(
    os.path.join(log_dir, r'C:\Users\neust\PycharmProjects\homework1_by_Kirsan\logs\utils.log'), mode='w')
utils_file_handler = logging.FileHandler(
    os.path.join(log_dir, r'C:\Users\neust\PycharmProjects\homework1_by_Kirsan\logs\utils.log'), encoding='utf-8')
utils_file_handler.setLevel(logging.DEBUG)

# Создаем форматтер и добавляем его в обработчик
utils_file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
utils_file_handler.setFormatter(utils_file_formatter)

# Добавляем обработчик в логер
utils_logger.addHandler(utils_file_handler)


def load_transactions(filename: str) -> List[Dict[str, Any]]:
    utils_logger.debug(f'Загрузка транзакций из файла: {filename}')
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            transactions = json.load(file)
            utils_logger.info(f'Успешно загружено {len(transactions)} транзакций.')
            return transactions
    except FileNotFoundError:
        utils_logger.error(f'Файл не найден: {filename}')
        return []
    except json.JSONDecodeError:
        utils_logger.error(f'Ошибка декодирования JSON в файле: {filename}')
        return []


def main():
    utils_logger.info('Запуск функции main.')
    # Загрузка транзакции
    transactions = load_transactions(r'C:\Users\neust\PycharmProjects\homework1_by_Kirsan\data\operations.json')
    utils_logger.debug(f'Количество загруженных транзакций: {len(transactions)}')

    # Конвертация суммы транзакций в рубли и выводи результата
    for transaction in transactions:
        try:
            amount_in_rub = convert_to_rub(transaction)
            print(f"Transaction ID: {transaction['id']}, Amount in RUB: {amount_in_rub:.2f}")
            utils_logger.info(f'Успешно конвертирована '
                              f'транзакция ID: {transaction["id"]}, сумма в RUB: {amount_in_rub:.2f}')
        except Exception as e:
            print(f"Failed to convert transaction ID: {transaction['id']}. Error: {e}")
            utils_logger.error(f'Ошибка конвертации транзакции ID: {transaction["id"]}. Ошибка: {e}')
    utils_logger.info('Завершение выполнения функции main.')


if __name__ == "__main__":
    main()
