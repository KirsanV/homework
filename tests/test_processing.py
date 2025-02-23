from typing import Dict, List

import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.fixture
def sample_data() -> List[Dict[str, str]]:
    """Фикстура для предоставления тестовых данных."""
    return [
        {"state": "EXECUTED", "date": "2023-01-01T12:00:00"},
        {"state": "PENDING", "date": "2023-01-02T12:00:00"},
        {"state": "EXECUTED", "date": "2023-01-03T12:00:00"},
    ]


def test_filter_by_state(sample_data: List[Dict[str, str]]) -> None:
    """Тестирование фильтрации списка словарей по заданному статусу state."""
    result = filter_by_state(sample_data, "EXECUTED")
    assert len(result) == 2
    assert all(item['state'] == "EXECUTED" for item in result)


def test_sort_by_date(sample_data: List[Dict[str, str]]) -> None:
    """Тестирование сортировки списка словарей по датам."""
    result = sort_by_date(sample_data)
    assert result[0]['date'] == "2023-01-03T12:00:00"
    assert result[1]['date'] == "2023-01-02T12:00:00"
    assert result[2]['date'] == "2023-01-01T12:00:00"
