from src.masks import get_mask_account, get_mask_card_number

card_number = "1234567812345678"
account_number = "1234567890123456"

masked_card = get_mask_card_number(card_number)
masked_account = get_mask_account(account_number)

print("Замаскированный номер карты:", masked_card)
print("Замаскированный номер счета:", masked_account)
