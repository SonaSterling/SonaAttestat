#!/usr/bin/env python3
"""
Currency Converter - Конвертер валют
Графическое приложение для конвертации валют с использованием внешнего API

Автор: [Ваше Имя Фамилия]
Дата: 2024
"""
import tkinter as tk
from currency_converter import CurrencyConverterApp

def main():
    """Главная функция запуска приложения"""
    root = tk.Tk()
    app = CurrencyConverterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
