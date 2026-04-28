"""
Модуль для работы с внешним API курсов валют
"""
import requests
import json
from datetime import datetime

class CurrencyAPI:
    """Клиент для получения курсов валют"""
    
    # Бесплатный API без ключа (для тестирования)
    # Документация: https://exchangerate-api.com
    BASE_URL = "https://api.exchangerate-api.com/v4/latest/"
    
    # Альтернативный API (требует ключ, но бесплатный)
    # Получить ключ: https://app.exchangerate-api.com/sign-up
    # PRIVATE_URL = "https://v6.exchangerate-api.com/v6/YOUR_API_KEY/latest/"
    
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.cache = {}
        self.last_update = None
    
    def get_exchange_rate(self, from_currency, to_currency):
        """
        Получает курс обмена между двумя валютами
        
        Args:
            from_currency (str): Исходная валюта (например, "USD")
            to_currency (str): Целевая валюта (например, "EUR")
        
        Returns:
            float: Курс обмена или None при ошибке
        """
        try:
            # Используем открытое API (не требует ключа)
            url = f"{self.BASE_URL}{from_currency}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            rates = data.get("rates", {})
            
            if to_currency in rates:
                return rates[to_currency]
            else:
                print(f"Валюта {to_currency} не найдена")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Ошибка API: {e}")
            return None
    
    def get_supported_currencies(self):
        """
        Получает список поддерживаемых валют
        
        Returns:
            list: Список кодов валют
        """
        try:
            url = f"{self.BASE_URL}USD"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            return sorted(data.get("rates", {}).keys())
        except:
            # Возвращаем базовый список в случае ошибки
            return ["USD", "EUR", "RUB", "GBP", "JPY", "CNY", "KZT", "UAH", "BYN", "TRY"]
