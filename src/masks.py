import logging
import os

# Настройка логирования для модуля masks
log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Создаем логер
masks_logger = logging.getLogger('masks')
masks_logger.setLevel(logging.DEBUG)

# Создаем обработчик для записи логов в файл
masks_file_handler = logging.FileHandler(
    os.path.join(log_dir, r'C:\Users\neust\PycharmProjects\homework1_by_Kirsan\logs\masks.log'), mode='w')
masks_file_handler = logging.FileHandler(
    os.path.join(log_dir, r'C:\Users\neust\PycharmProjects\homework1_by_Kirsan\logs\masks.log'), encoding='utf-8')
masks_file_handler.setLevel(logging.DEBUG)

# Создаем форматтер и добавляем его в обработчик
masks_file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
masks_file_handler.setFormatter(masks_file_formatter)

# Добавляем обработчик в логер
masks_logger.addHandler(masks_file_handler)


def get_mask_card_number(card_number: str) -> str:
    masks_logger.info(f'Получен номер карты: {card_number}')
    if not card_number:
        masks_logger.warning('Пустой номер карты')
        return ""

    card_number = ''.join(filter(str.isdigit, card_number))

    if len(card_number) <= 12:
        masks_logger.error('Это не номер карты')
        return "Это не номер карты"

    # Логируем успешные случаи
    masks_logger.info(f'Маскируем номер карты: {card_number}')

    if len(card_number) == 13:
        return f"{card_number[:4]} {card_number[4:6]}** * **{card_number[-2:]}"
    elif len(card_number) == 14:
        return f"{card_number[:4]} {card_number[4:6]}** ** *{card_number[-3:]}"
    elif len(card_number) == 15:
        return f"{card_number[:4]} {card_number[4:6]}** *** {card_number[-4:]}"

    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"


def get_mask_account(account_number: str) -> str:
    masks_logger.info(f'Получен номер счета: {account_number}')
    if not account_number:
        masks_logger.warning('Пустой номер счета')
        return ""

    # Убедимся, что номер счета состоит только из цифр
    account_number = ''.join(filter(str.isdigit, account_number))

    if len(account_number) <= 4:
        masks_logger.error('Это не номер счета')
        return "Это не номер счета"

    masked_part = '*' * (len(account_number) - 4)  # Маскируем все, кроме последних 4
    masks_logger.info(f'Маскируем номер счета: {account_number}')
    return f"{masked_part}{account_number[-4:]}"
