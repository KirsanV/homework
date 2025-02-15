def filter_by_state(data, state='EXECUTED'):
    return [item for item in data if item.get('state') == state]

    """Функция фильтрующая список словарей по ключу 'state'"""

def sort_by_date(data, descending=True):
    return sorted(data, key=lambda x: x['date'], reverse=descending)

    """Функция фильтрующая список словарей по дате"""


filter_function_check = [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
     {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
     {'id': 594226727, 'state': 'EXECUTED', 'date': '2018-09-12T21:27:25.241689'},
     {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
     ]
date_sort_check = [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
     {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
     {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
     {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
     ]


print(filter_by_state(filter_function_check))
print(sort_by_date(date_sort_check))
