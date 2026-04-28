"""
Модуль для управления историей конвертаций (JSON)
"""
import json
import os
from datetime import datetime

class HistoryManager:
    """Управление сохранением и загрузкой истории"""
    
    def __init__(self, filename="history.json"):
        self.filename = filename
        self.history = self.load_history()
    
    def load_history(self):
        """Загружает историю из JSON файла"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Ошибка загрузки истории: {e}")
                return []
        return []
    
    def save_history(self):
        """Сохраняет историю в JSON файл"""
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
            return True
        except IOError as e:
            print(f"Ошибка сохранения истории: {e}")
            return False
    
    def add_record(self, from_currency, to_currency, amount, result, rate):
        """
        Добавляет запись в историю
        
        Args:
            from_currency (str): Исходная валюта
            to_currency (str): Целевая валюта
            amount (float): Сумма
            result (float): Результат конвертации
            rate (float): Курс обмена
        """
        record = {
            "id": len(self.history) + 1,
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "from_currency": from_currency,
            "to_currency": to_currency,
            "amount": amount,
            "result": round(result, 2),
            "rate": round(rate, 4),
            "formatted": f"{amount} {from_currency} = {round(result, 2)} {to_currency}"
        }
        self.history.append(record)
        self.save_history()
        return record
    
    def clear_history(self):
        """Очищает историю"""
        self.history = []
        self.save_history()
    
    def get_history(self):
        """Возвращает всю историю"""
        return self.history
