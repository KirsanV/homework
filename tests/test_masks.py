import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize("card_number, expected", [
    ("1234567890123456", "1234 56** **** 3456"),
    ("1234", "Это не номер карты"),
    ("", ""),
    ("1234567890123", "1234 56** * **23"),
    ("12345678901234", "1234 56** ** *234"),
    ("123456789012345", "1234 56** *** 2345"),
])
def test_get_mask_card_number(card_number: str, expected: str) -> None:
    """Тестирование правильности маскирования номера карты."""
    assert get_mask_card_number(card_number) == expected


@pytest.mark.parametrize("account_number, expected", [
    ("123456789012", "********9012"),    # ожидается: ********9012
    ("1234", "Это не номер счета"),      # ожидается: "Это не номер счета"
    ("", ""),                            # ожидается: ''
])
def test_get_mask_account(account_number: str, expected: str) -> None:
    """Тестирование правильности маскирования номера счета."""
    assert get_mask_account(account_number) == expected
