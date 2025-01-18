import json
import requests
from config import keys

class ApiException(Exception): # Ловим ошибки
    pass

class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ApiException(f'Невозможно перевести одинаковые валюты {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ApiException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ApiException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ApiException(f'Не удалось обработать количество {amount}')

        api = requests.get(f'https://v6.exchangerate-api.com/v6/c9029a1cddc85e56a8dd861f/pair/{quote_ticker}/{base_ticker}/{amount}')
        if api.status_code == 200:
            data = api.json()
            return data['conversion_result']
        else:
            raise ApiException(f'Ошибка запроса: {api.status_code}')