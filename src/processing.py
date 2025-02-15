from typing import Dict, List


def filter_by_state(data: List[Dict[str, str]], state: str = 'EXECUTED') -> List[Dict[str, str]]:
    """Функция фильтрующая список словарей по ключу 'state'"""
    return [item for item in data if item.get('state') == state]


def sort_by_date(data: List[Dict[str, str]], descending: bool = True) -> List[Dict[str, str]]:
    """Функция фильтрующая список словарей по дате"""
    return sorted(data, key=lambda x: x['date'], reverse=descending)
