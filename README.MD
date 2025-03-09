# Проект "Processing" и "generators"
## Описание проекта
Добавление новых функциональностей для существующего проекта
в рамках домашней работы по курсу разработка на Python 
(продвинутый GIT).
Данный функционал предполагает: 
прием в качестве вводных данных списка словарей
и его дальнейшую сортировку по критериям (наличие ключа 'state : EXECUTED' и дата). 
V2.0 
Добавлен новый модуль в "generators".
В котором реализованы новые функции-генераторы
filter_by_currency - принимает на вход список словарей, представляющих транзакции.
Функция должна возвращать итератор, который поочередно выдает транзакции, 
где валюта операции соответствует заданной (например, USD).
transaction_descriptions - который принимает список словарей с транзакциями и 
возвращает описание каждой операции по очереди.
card_number_generator - который выдает номера банковских карт в формате 
XXXX XXXX XXXX XXXX.
Добавлен новый модуль decorators.
В котором реализована функция записи логов

## Тестирование
В проект были добавлены тесты(проверки). Покрытие 99%.
Папка tests/ test_masks.py test_processing.py test_widget.py test_generators.py test_decorators.py

## Установка
1. Клонируйте репозиторий: git clone https://github.com/KirsanV/homework
## Использование
Импортируйте функции из модуля `processing` и используйте их для обработки данных.
### Примеры для работы с сортировщиком по ключу 'state'
    [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}, 
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}, 
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}, 
    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ]
### Примеры для работы с сортировщиком по дате
    [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}, 
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}, 
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}, 
    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ]

### Примеры для работы генератора для фильтрации транзакций по указанной валюте
    transactions = (
    [
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
)

Функция вернет из предложенного списка все транзакции в USD, если таковой критерий задать.
        assert next(usd_transactions) == transactions[0]
        assert next(usd_transactions) == transactions[1]
        assert next(usd_transactions) == transactions[3]
### Примеры для работы генератора для выдачи описания каждой транзакции

Функция вернет описание каждой операции по очереди.

    assert next(descriptions) == "Перевод организации"
    assert next(descriptions) == "Перевод со счета на счет"
    assert next(descriptions) == "Перевод со счета на счет"
    assert next(descriptions) == "Перевод с карты на карту"
    assert next(descriptions) == "Перевод организации"


### Примеры для работы генератора который выдает номера банковских карт в формате XXXX XXXX XXXX XXXX
Генератор может сгенерировать номера карт в заданном диапазоне от 0000 0000 0000 0001 до 9999 9999 9999 9999.
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
    "from": "0000 0000 0000 0000",
    "to": "0000 0000 0000 0001"
}
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
    "from": "0000 0000 0000 0002",
    "to": "0000 0000 0000 0003"
}
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
    "from": "0000 0000 0000 0004",
    "to": "0000 0000 0000 0005"
}
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
    "from": "0000 0000 0000 0006",
    "to": "0000 0000 0000 0007"
}
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
    }

### Примеры для работы декоратора
На примере ниже указаны записи об успешных и неуспешных выполнений функции
2025-03-09 08:55:02,504 - INFO - successful_function ok
2025-03-09 08:55:02,504 - INFO - successful_function ok
2025-03-09 08:55:02,507 - INFO - successful_function ok
2025-03-09 08:55:02,507 - INFO - successful_function ok
2025-03-09 08:55:02,517 - ERROR - successful_function error: TypeError. Inputs: (1, 's'), {}
2025-03-09 08:55:02,517 - ERROR - successful_function error: TypeError. Inputs: (1, 's'), {}