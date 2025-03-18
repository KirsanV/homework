from typing import List, Dict, Tuple

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions

# Предоставленный список транзакций
@pytest.fixture
def transactions() -> List[Dict]:
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702"
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188"
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160"
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {
                "amount": "56883.54",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229"
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {
                "amount": "67314.70",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            },
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657"
        }
    ]



def test_filter_by_currency(transactions) -> None:
    usd_transactions = filter_by_currency(transactions, "USD")

    assert next(usd_transactions) == transactions[0]
    assert next(usd_transactions) == transactions[1]
    assert next(usd_transactions) == transactions[3]
    with pytest.raises(StopIteration):
        next(usd_transactions)

    eur_transactions = filter_by_currency(transactions, "EUR")
    with pytest.raises(StopIteration):
        next(eur_transactions)

    empty_transactions: List = []
    empty_generator = filter_by_currency(empty_transactions, "USD")
    with pytest.raises(StopIteration):
        next(empty_generator)


def test_transaction_descriptions(transactions) -> None:
    descriptions = transaction_descriptions(transactions)
    assert next(descriptions) == "Перевод организации"
    assert next(descriptions) == "Перевод со счета на счет"
    assert next(descriptions) == "Перевод со счета на счет"
    assert next(descriptions) == "Перевод с карты на карту"
    assert next(descriptions) == "Перевод организации"

    # Проверка с пустым списком
    empty_descriptions = transaction_descriptions([])
    with pytest.raises(StopIteration):
        next(empty_descriptions)


# Фикстура для простого диапазона
@pytest.fixture
def simple_test_range() -> Tuple[int, int]:
    return (1, 5)


# Фикстура для крайних случаев
@pytest.fixture
def edge_case_range() -> Tuple[int, int]:
    return (0, 0)


# Фикстура для большого диапазона чисел
@pytest.fixture
def large_number_range() -> Tuple[int, int]:
    return (999999999999999, 1000000000000000)


# Тест для генератора с простым диапазоном
def test_card_number_generator(simple_test_range: Tuple[int, int]) -> None:
    start, end = simple_test_range
    expected_numbers = [
        '0000 0000 0000 0001',
        '0000 0000 0000 0002',
        '0000 0000 0000 0003',
        '0000 0000 0000 0004',
        '0000 0000 0000 0005'
    ]
    generated_numbers = list(card_number_generator(start, end))

    assert generated_numbers == expected_numbers


# Тест для генератора с крайними случаями
def test_card_number_generator_edge_cases(edge_case_range: Tuple[int, int]) -> None:
    start, end = edge_case_range

    expected_number = ['0000 0000 0000 0000']

    generated_numbers = list(card_number_generator(start, end))

    assert generated_numbers == expected_number


# Тест для генератора с большими числами
def test_card_number_generator_large_numbers(large_number_range: Tuple[int, int]) -> None:
    start, end = large_number_range
    expected_numbers = [
        f"{start:016d}"[:4] + " " + f"{start:016d}"[4:8] + " " + f"{start:016d}"[8:12] + " " + f"{start:016d}"[12:],
        f"{end:016d}"[:4] + " " + f"{end:016d}"[4:8] + " " + f"{end:016d}"[8:12] + " " + f"{end:016d}"[12:],
    ]
    generated_numbers = list(card_number_generator(start, end))
    assert len(generated_numbers) == len(expected_numbers)  # Проверка количества
    assert generated_numbers == expected_numbers  # Проверка содержимого списков


# Параметризованный тест для форматирования номеров карт
@pytest.mark.parametrize("start, end, expected", [
    (1234, 1236, [
        '0000 0000 0000 1234',
        '0000 0000 0000 1235',
        '0000 0000 0000 1236',
    ]),
    (10, 12, [
        '0000 0000 0000 0010',
        '0000 0000 0000 0011',
        '0000 0000 0000 0012',
    ])
])
def test_card_number_formatting(start: int, end: int, expected: List[str]) -> None:
    generated_numbers = list(card_number_generator(start, end))
    assert generated_numbers == expected
