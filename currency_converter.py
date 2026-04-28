"""
Главный класс приложения Currency Converter
"""
import tkinter as tk
from tkinter import ttk, messagebox
from api_client import CurrencyAPI
from history_manager import HistoryManager

class CurrencyConverterApp:
    """Основное GUI приложение для конвертации валют"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter - Конвертер валют")
        self.root.geometry("750x600")
        self.root.resizable(False, False)
        
        # Инициализация компонентов
        self.api = CurrencyAPI()
        self.history_manager = HistoryManager()
        
        # Получение списка валют с обработкой ошибок
        try:
            self.currencies = self.api.get_supported_currencies()
            if not self.currencies:
                self.currencies = ["USD", "EUR", "RUB", "GBP", "JPY", "CNY", "KZT", "UAH"]
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось получить список валют.\nИспользуются стандартные валюты.\nОшибка: {e}")
            self.currencies = ["USD", "EUR", "RUB", "GBP", "JPY", "CNY", "KZT", "UAH"]
        
        # Создание интерфейса
        self.create_widgets()
        
        # Загрузка истории
        self.refresh_history_table()
    
    def create_widgets(self):
        """Создаёт все элементы интерфейса"""
        
        # Главный контейнер
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # ===== Верхняя панель конвертации =====
        convert_frame = tk.LabelFrame(main_frame, text="Конвертация валют", padx=15, pady=15, font=("Arial", 12, "bold"))
        convert_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Сумма
        tk.Label(convert_frame, text="Сумма:", font=("Arial", 11)).grid(row=0, column=0, sticky="w", pady=5)
        self.amount_entry = tk.Entry(convert_frame, width=15, font=("Arial", 12))
        self.amount_entry.grid(row=0, column=1, padx=(10, 20), pady=5)
        self.amount_entry.bind("<KeyRelease>", self.validate_amount)
        
        # Из валюты
        tk.Label(convert_frame, text="Из валюты:", font=("Arial", 11)).grid(row=0, column=2, sticky="w", pady=5)
        self.from_currency = ttk.Combobox(convert_frame, values=self.currencies, width=8, font=("Arial", 11))
        self.from_currency.set("USD")
        self.from_currency.grid(row=0, column=3, padx=10, pady=5)
        
        # В валюту
        tk.Label(convert_frame, text="В валюту:", font=("Arial", 11)).grid(row=0, column=4, sticky="w", pady=5)
        self.to_currency = ttk.Combobox(convert_frame, values=self.currencies, width=8, font=("Arial", 11))
        self.to_currency.set("EUR")
        self.to_currency.grid(row=0, column=5, padx=10, pady=5)
        
        # Кнопка конвертации
        self.convert_btn = tk.Button(convert_frame, text="🔄 Конвертировать", command=self.convert,
                                     bg="#4CAF50", fg="white", font=("Arial", 11, "bold"), 
                                     width=15, height=1)
        self.convert_btn.grid(row=0, column=6, padx=20, pady=5)
        
        # Результат
        self.result_label = tk.Label(convert_frame, text="", font=("Arial", 14, "bold"), fg="#2196F3")
        self.result_label.grid(row=1, column=0, columnspan=7, pady=15)
        
        # Сообщение об ошибке
        self.error_label = tk.Label(convert_frame, text="", font=("Arial", 10), fg="red")
        self.error_label.grid(row=2, column=0, columnspan=7)
        
        # ===== Панель информации =====
        info_frame = tk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.rate_label = tk.Label(info_frame, text="Курс: -", font=("Arial", 10), fg="gray")
        self.rate_label.pack(side=tk.LEFT)
        
        self.clear_btn = tk.Button(info_frame, text="🗑 Очистить историю", command=self.clear_history,
                                   bg="#FF9800", fg="white", font=("Arial", 9))
        self.clear_btn.pack(side=tk.RIGHT)
        
        # ===== Таблица истории =====
        history_frame = tk.LabelFrame(main_frame, text="История конвертаций", padx=10, pady=10, font=("Arial", 12, "bold"))
        history_frame.pack(fill=tk.BOTH, expand=True)
        
        # Создание таблицы
        columns = ("datetime", "from_currency", "to_currency", "amount", "result", "rate")
        self.history_tree = ttk.Treeview(history_frame, columns=columns, show="headings", height=12)
        
        # Настройка заголовков
        self.history_tree.heading("datetime", text="Дата и время")
        self.history_tree.heading("from_currency", text="Из")
        self.history_tree.heading("to_currency", text="В")
        self.history_tree.heading("amount", text="Сумма")
        self.history_tree.heading("result", text="Результат")
        self.history_tree.heading("rate", text="Курс")
        
        # Настройка ширины колонок
        self.history_tree.column("datetime", width=150)
        self.history_tree.column("from_currency", width=70)
        self.history_tree.column("to_currency", width=70)
        self.history_tree.column("amount", width=100)
        self.history_tree.column("result", width=100)
        self.history_tree.column("rate", width=100)
        
        # Прокрутка
        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def validate_amount(self, event=None):
        """Валидация ввода суммы"""
        amount_str = self.amount_entry.get().strip()
        
        if amount_str == "":
            self.error_label.config(text="")
            return True
        
        # Разрешаем только числа и точку
        try:
            amount = float(amount_str)
            if amount <= 0:
                self.error_label.config(text="⚠️ Сумма должна быть положительным числом!")
                return False
            else:
                self.error_label.config(text="✓ Валидная сумма", fg="green")
                return True
        except ValueError:
            self.error_label.config(text="❌ Введите корректное число (например: 100.50)", fg="red")
            return False
    
    def convert(self):
        """Выполняет конвертацию валют"""
        # Валидация суммы
        amount_str = self.amount_entry.get().strip()
        if not amount_str:
            messagebox.showwarning("Предупреждение", "Введите сумму для конвертации")
            return
        
        try:
            amount = float(amount_str)
            if amount <= 0:
                messagebox.showwarning("Предупреждение", "Сумма должна быть положительным числом")
                return
        except ValueError:
            messagebox.showwarning("Предупреждение", "Введите корректное число (используйте точку как разделитель)")
            return
        
        # Получаем выбранные валюты
        from_curr = self.from_currency.get()
        to_curr = self.to_currency.get()
        
        if not from_curr or not to_curr:
            messagebox.showwarning("Предупреждение", "Выберите валюты из списка")
            return
        
        # Индикатор загрузки
        self.convert_btn.config(state="disabled", text="⏳ Загрузка...")
        self.root.update()
        
        # Получаем курс с обработкой ошибок
        try:
            rate = self.api.get_exchange_rate(from_curr, to_curr)
        except Exception as e:
            self.convert_btn.config(state="normal", text="🔄 Конвертировать")
            messagebox.showerror("Ошибка API", f"Не удалось подключиться к серверу курсов.\n\nПроверьте интернет-соединение.\n\nДетали: {e}")
            return
        
        self.convert_btn.config(state="normal", text="🔄 Конвертировать")
        
        if rate is None:
            messagebox.showerror("Ошибка", f"Не удалось получить курс {from_curr} → {to_curr}\n\nВозможные причины:\n• Валюта не поддерживается\n• API временно недоступен")
            return
        
        # Вычисляем результат
        result = amount * rate
        
        # Обновляем интерфейс
        self.result_label.config(text=f"💰 {amount:.2f} {from_curr} = {result:.2f} {to_curr}")
        self.rate_label.config(text=f"📊 Курс: 1 {from_curr} = {rate:.4f} {to_curr}")
        
        # Сохраняем в историю
        self.history_manager.add_record(from_curr, to_curr, amount, result, rate)
        
        # Обновляем таблицу истории
        self.refresh_history_table()
    
    def refresh_history_table(self):
        """Обновляет таблицу истории"""
        # Очищаем таблицу
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # Добавляем записи
        for record in self.history_manager.get_history():
            self.history_tree.insert("", tk.END, values=(
                record["datetime"],
                record["from_currency"],
                record["to_currency"],
                f"{record['amount']:.2f}",
                f"{record['result']:.2f}",
                f"{record['rate']:.4f}"
            ))
    
    def clear_history(self):
        """Очищает историю с подтверждением"""
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить всю историю?"):
            self.history_manager.clear_history()
            self.refresh_history_table()
            messagebox.showinfo("Успех", "История конвертаций очищена")
