from datetime import datetime


def mask_account_card(info: str) -> str:
    if info.startswith("Счет"):
        return "Cчет **" + info[-4:]
    else:
        parts = info.split()
        card_type = " ".join(parts[:-1])
        card_number = parts[-1]
        return f"{card_type} {card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"

    """ Функция для маскирования номера счета и карты"""


def get_date(date_string: str) -> str:
    date_time_obj = datetime.fromisoformat(date_string)
    return date_time_obj.strftime("%d.%m.%Y")

    """Функция для преобразования даты в формат 'ДД.ММ.ГГГГ'"""


print(mask_account_card("Visa Gold 5999414228426353"))
print(mask_account_card("Счет 73654108430135874305"))
print(get_date("2024-03-11T02:26:18.671407"))
