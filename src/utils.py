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
log_file_path = os.path.join(os.path.dirname(__file__), '..', log_dir, 'utils.log')
utils_file_handler = logging.FileHandler(log_file_path, mode='w', encoding='utf-8')

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
    transactions_file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'operations.json')
    transactions = load_transactions(transactions_file_path)
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
