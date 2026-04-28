#!/usr/bin/env python3
"""
Currency Converter - Конвертер валют
Графическое приложение для конвертации валют с использованием внешнего API

Автор: Зубанова Софья
Email: sona33222111@gmail.com


Дата: 2026
"""
import tkinter as tk
from currency_converter import CurrencyConverterApp

def main():
    """Главная функция запуска приложения"""
    try:
        root = tk.Tk()
        app = CurrencyConverterApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Критическая ошибка при запуске: {e}")
        import sys
        sys.exit(1)

if __name__ == "__main__":
    main()
