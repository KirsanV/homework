def mask_account_card(info):
    if info.startswith("Счет"):
        # Маскировка для счета
        return 'Cчет **' + info[-4:]
    else:
        # Маскировка для карт
        parts = info.split()
        card_type = ' '.join(parts[:-1])
        card_number = parts[-1]
        return f"{card_type} {card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"



def get_date(date_string):
    from datetime import datetime
    date_time_obj = datetime.fromisoformat(date_string)
    return date_time_obj.strftime("%d.%m.%Y")

print(mask_account_card("Maestro 1596837868705199"))
print(mask_account_card("Счет 35383033474447895560"))
print(get_date("2024-03-11T02:26:18.671407"))