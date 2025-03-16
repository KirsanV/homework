import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv

load_dotenv()


def convert_to_rub(transaction: Dict[str, Any]) -> float:
    """
    Конвертация суммы в транзакции из заданной валюты в рубли (RUB).
    """
    amount = float(transaction['operationAmount']['amount'])
    currency_code = transaction['operationAmount']['currency']['code']

    if currency_code == "RUB":
        return amount

    access_token = os.getenv('API_ACCESS_TOKEN')
    response = requests.get(f'https://api.apilayer.com/exchangerates_data/latest?base={currency_code}&symbols=RUB',
                            headers={"apikey": access_token})

    if response.status_code == 200:
        data = response.json()
        exchange_rate = data['rates']['RUB']
        return amount * exchange_rate
    else:
        raise Exception(f"Error fetching exchange rates: {response.status_code}")
