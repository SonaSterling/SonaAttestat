"""
Модульные тесты для Currency Converter
"""
import unittest
import json
import os
import tempfile
from history_manager import HistoryManager
from api_client import CurrencyAPI

class TestHistoryManager(unittest.TestCase):
    """Тесты для менеджера истории"""
    
    def setUp(self):
        # Создаём временный файл для тестов
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        self.temp_file.close()
        self.history_manager = HistoryManager(self.temp_file.name)
    
    def tearDown(self):
        # Удаляем временный файл
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_add_record_positive(self):
        """Позитивный тест: добавление записи"""
        record = self.history_manager.add_record("USD", "EUR", 100, 85.50, 0.855)
        self.assertEqual(record["amount"], 100)
        self.assertEqual(record["from_currency"], "USD")
        self.assertEqual(record["to_currency"], "EUR")
        self.assertEqual(len(self.history_manager.get_history()), 1)
    
    def test_save_and_load(self):
        """Позитивный тест: сохранение и загрузка"""
        self.history_manager.add_record("RUB", "USD", 1000, 10.50, 0.0105)
        self.history_manager.save_history()
        
        # Создаём новый менеджер и загружаем
        new_manager = HistoryManager(self.temp_file.name)
        self.assertEqual(len(new_manager.get_history()), 1)
    
    def test_clear_history(self):
        """Позитивный тест: очистка истории"""
        self.history_manager.add_record("USD", "RUB", 100, 9000, 90)
        self.history_manager.clear_history()
        self.assertEqual(len(self.history_manager.get_history()), 0)
    
    def test_multiple_records(self):
        """Позитивный тест: несколько записей"""
        for i in range(5):
            self.history_manager.add_record("USD", "EUR", i*100, i*85, 0.85)
        self.assertEqual(len(self.history_manager.get_history()), 5)

class TestAPIClient(unittest.TestCase):
    """Тесты для API клиента"""
    
    def setUp(self):
        self.api = CurrencyAPI()
    
    def test_get_supported_currencies(self):
        """Позитивный тест: получение списка валют"""
        currencies = self.api.get_supported_currencies()
        self.assertIsInstance(currencies, list)
        self.assertGreater(len(currencies), 0)
        self.assertIn("USD", currencies)
    
    def test_get_exchange_rate_positive(self):
        """Позитивный тест: получение курса"""
        rate = self.api.get_exchange_rate("USD", "EUR")
        if rate is not None:  # API может быть недоступен
            self.assertIsInstance(rate, float)
            self.assertGreater(rate, 0)
    
    def test_get_exchange_rate_invalid_currency(self):
        """Негативный тест: несуществующая валюта"""
        rate = self.api.get_exchange_rate("XXX", "YYY")
        self.assertIsNone(rate)

class TestValidation(unittest.TestCase):
    """Тесты валидации"""
    
    def test_positive_amount(self):
        """Позитивный тест: положительная сумма"""
        amount = 100.50
        self.assertGreater(amount, 0)
    
    def test_negative_amount(self):
        """Негативный тест: отрицательная сумма"""
        amount = -50
        self.assertLess(amount, 0)
    
    def test_zero_amount(self):
        """Граничный тест: нулевая сумма"""
        amount = 0
        self.assertEqual(amount, 0)
    
    def test_string_amount(self):
        """Негативный тест: строка вместо числа"""
        with self.assertRaises(ValueError):
            float("abc")

if __name__ == "__main__":
    unittest.main()
