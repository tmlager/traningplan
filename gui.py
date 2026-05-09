import tkinter as tk
from tkinter import ttk, messagebox
from training_planner import TrainingPlanner

class TrainingPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner - План тренировок")
        self.root.geometry("950x650")
        self.root.resizable(True, True)
        
        # Инициализация
        try:
            self.planner = TrainingPlanner()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")
            self.root.quit()
            return
        
        self.setup_ui()
        self.update_table()
        self.update_statistics()
    
    def setup_ui(self):
        # Основной контейнер
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # ===== Левая панель: Добавление тренировки =====
        add_frame = ttk.LabelFrame(main_frame, text="Добавить тренировку", padding="15")
        add_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 15))
        
        # Дата
        ttk.Label(add_frame, text="📅 Дата (ГГГГ-ММ-ДД):", font=("Arial", 10)).pack(anchor=tk.W, pady=(0, 5))
        self.date_entry = ttk.Entry(add_frame, width=20, font=("Arial", 11))
        self.date_entry.pack(fill=tk.X, pady=(0, 10))
        self.date_entry.insert(0, "2026-05-09")
        
        # Тип тренировки
        ttk.Label(add_frame, text="🏋️ Тип тренировки:", font=("Arial", 10)).pack(anchor=tk.W, pady=(0, 5))
        self.type_var = tk.StringVar(value="Бег")
        self.type_combo = ttk.Combobox(add_frame, textvariable=self.type_var, 
                                        values=self.planner.get_training_types(),
                                        state="readonly", width=18)
        self.type_combo.pack(fill=tk.X, pady=(0, 10))
        
        # Длительность
        ttk.Label(add_frame, text="⏱️ Длительность (минуты):", font=("Arial", 10)).pack(anchor=tk.W, pady=(0, 5))
        self.duration_entry = ttk.Entry(add_frame, width=20, font=("Arial", 11))
        self.duration_entry.pack(fill=tk.X, pady=(0, 10))
        self.duration_entry.insert(0, "30")
        
        # Кнопка добавления
        self.add_btn = ttk.Button(add_frame, text="➕ Добавить тренировку", 
                                   command=self.add_training, width=25)
        self.add_btn.pack(pady=(10, 0))
        
        # Статистика
        stats_frame = ttk.LabelFrame(add_frame, text="📊 Статистика", padding="10")
        stats_frame.pack(fill=tk.X, pady=(20, 0))
        
        self.total_label = ttk.Label(stats_frame, text="Всего тренировок: 0")
        self.total_label.pack(anchor=tk.W, pady=2)
        
        self.total_minutes_label = ttk.Label(stats_frame, text="Общая длительность: 0 мин")
        self.total_minutes_label.pack(anchor=tk.W, pady=2)
        
        self.by_type_text = tk.Text(stats_frame, height=8, width=25, font=("Arial", 9))
        self.by_type_text.pack(fill=tk.X, pady=(5, 0))
        
        # ===== Правая панель: Просмотр и фильтрация =====
        view_frame = ttk.LabelFrame(main_frame, text="Тренировки", padding="10")
        view_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Фильтры
        filter_frame = ttk.Frame(view_frame)
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(filter_frame, text="Фильтр по типу:").pack(side=tk.LEFT, padx=5)
        self.filter_type_var = tk.StringVar(value="Все")
        self.filter_type_combo = ttk.Combobox(filter_frame, textvariable=self.filter_type_var,
                                               values=["Все"] + self.planner.get_training_types(),
                                               state="readonly", width=12)
        self.filter_type_combo.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(filter_frame, text="Фильтр по дате:").pack(side=tk.LEFT, padx=5)
        self.filter_date_entry = ttk.Entry(filter_frame, width=12)
        self.filter_date_entry.pack(side=tk.LEFT, padx=5)
        
        self.apply_filter_btn = ttk.Button(filter_frame, text="🔍 Применить фильтр", 
                                            command=self.apply_filter)
        self.apply_filter_btn.pack(side=tk.LEFT, padx=10)
        
        self.reset_filter_btn = ttk.Button(filter_frame, text="🔄 Сбросить", 
                                            command=self.reset_filter)
        self.reset_filter_btn.pack(side=tk.LEFT, padx=5)
        
        # Таблица тренировок
        columns = ("Дата", "Тип тренировки", "Длительность (мин)")
        self.tree = ttk.Treeview(view_frame, columns=columns, show="headings", height=20)
        
        self.tree.heading("Дата", text="📅 Дата")
        self.tree.heading("Тип тренировки", text="🏋️ Тип тренировки")
        self.tree.heading("Длительность (мин)", text="⏱️ Длительность (мин)")
        
        self.tree.column("Дата", width=120)
        self.tree.column("Тип тренировки", width=150)
        self.tree.column("Длительность (мин)", width=120)
        
        scrollbar = ttk.Scrollbar(view_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Кнопка удаления
        self.delete_btn = ttk.Button(view_frame, text="🗑 Удалить выбранную тренировку", 
                                      command=self.delete_training)
        self.delete_btn.pack(pady=(10, 0))
    
    def validate_gui_inputs(self) -> tuple:
        """
        Валидация ввода в GUI перед передачей в логику
        Возвращает (is_valid, date, training_type, duration, error_message)
        """
        date = self.date_entry.get().strip()
        training_type = self.type_var.get()
        duration_str = self.duration_entry.get().strip()
        
        # Проверка даты
        if not date:
            return False, None, None, None, "Введите дату!"
        
        # Проверка длительности
        if not duration_str:
            return False, None, None, None, "Введите длительность!"
        
        try:
            duration = float(duration_str)
        except ValueError:
            return False, None, None, None, "Длительность должна быть числом!"
        
        return True, date, training_type, duration, None
    
    def add_training(self):
        """Добавляет тренировку с валидацией в GUI"""
        # Валидация в GUI
        is_valid, date, training_type, duration, error_msg = self.validate_gui_inputs()
        
        if not is_valid:
            messagebox.showerror("Ошибка ввода", error_msg)
            return
        
        # Передаём в логику
        success, message = self.planner.add_training(date, training_type, duration)
        
        if success:
            messagebox.showinfo("Успех", message)
            # Очищаем поля
            self.duration_entry.delete(0, tk.END)
            self.duration_entry.insert(0, "30")
            self.update_table()
            self.update_statistics()
        else:
            messagebox.showerror("Ошибка", message)
    
    def apply_filter(self):
        """Применяет фильтры"""
        filter_type = self.filter_type_var.get()
        filter_date = self.filter_date_entry.get().strip()
        
        # Валидация даты фильтра
        if filter_date:
            is_valid, error_msg = TrainingPlanner.validate_date(filter_date)
            if not is_valid:
                messagebox.showerror("Ошибка фильтра", error_msg)
                return
        
        if filter_type == "Все":
            filter_type = None
        
        if not filter_date:
            filter_date = None
        
        filtered = self.planner.filter_by_both(filter_type, filter_date)
        self.update_table(filtered)
    
    def reset_filter(self):
        """Сбрасывает фильтры"""
        self.filter_type_var.set("Все")
        self.filter_date_entry.delete(0, tk.END)
        self.update_table()
    
    def update_table(self, trainings=None):
        """Обновляет таблицу"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if trainings is None:
            trainings = self.planner.get_all_trainings()
        
        for training in trainings:
            self.tree.insert("", tk.END, values=(
                training["date"],
                training["type"],
                training["duration"]
            ))
    
    def update_statistics(self):
        """Обновляет статистику"""
        stats = self.planner.get_statistics()
        
        self.total_label.config(text=f"Всего тренировок: {stats['total']}")
        self.total_minutes_label.config(text=f"Общая длительность: {stats['total_minutes']} мин")
        
        self.by_type_text.delete(1.0, tk.END)
        if stats["by_type"]:
            for t_type, count in stats["by_type"].items():
                self.by_type_text.insert(tk.END, f"• {t_type}: {count}\n")
        else:
            self.by_type_text.insert(tk.END, "Нет данных")
    
    def delete_training(self):
        """Удаляет выбранную тренировку"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите тренировку для удаления!")
            return
        
        item = selected[0]
        index = self.tree.index(item)
        
        if messagebox.askyesno("Подтверждение", "Удалить эту тренировку?"):
            self.planner.delete_training(index)
            self.update_table()
            self.update_statistics()