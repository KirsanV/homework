def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер карты, оставляя видимыми участки в зависимости от длины номера.
    """
    if not card_number:
        return ""
    # Убедимся, что номер карты состоит только из цифр
    card_number = ''.join(filter(str.isdigit, card_number))

    if len(card_number) <= 12:
        return "Это не номер карты"

    elif len(card_number) == 13:
        return f"{card_number[:4]} {card_number[4:6]}** * **{card_number[-2:]}"

    elif len(card_number) == 14:
        return f"{card_number[:4]} {card_number[4:6]}** ** *{card_number[-3:]}"

    elif len(card_number) == 15:
        return f"{card_number[:4]} {card_number[4:6]}** *** {card_number[-4:]}"
    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер счета, оставляя видимыми только последние 4 цифры.
    """
    if not account_number:
        return ""

    # Убедимся, что номер счета состоит только из цифр
    account_number = ''.join(filter(str.isdigit, account_number))

    if len(account_number) <= 4:
        return "Это не номер счета"

    masked_part = '*' * (len(account_number) - 4)  # Маскируем все, кроме последних 4
    return f"{masked_part}{account_number[-4:]}"
