import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize("info, expected", [
    ("Счет 123456789012", "Cчет **9012"),
    ("Visa 1234567890123456", "Visa 1234 56** **** 3456"),
])
def test_mask_account_card(info: str, expected: str) -> None:
    """Тестирование маскирования номера счета и карты."""
    assert mask_account_card(info) == expected


@pytest.mark.parametrize("date_string, expected", [
    ("2023-01-01T12:00:00", "01.01.2023"),
    ("2023-12-31T23:59:59", "31.12.2023"),
])
def test_get_date(date_string: str, expected: str) -> None:
    """Тестирование правильности преобразования даты."""
    assert get_date(date_string) == expected
