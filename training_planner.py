import json
from datetime import datetime
from typing import List, Dict, Tuple, Optional

class TrainingPlanner:
    def __init__(self, filename: str = "trainings.json"):
        self.filename = filename
        self.trainings: List[Dict] = []
        self.training_types = ["Бег", "Силовая", "Йога", "Велосипед", "Плавание", "Растяжка", "Кардио", "Футбол"]
        self.load_data()
    
    @staticmethod
    def validate_date(date_str: str) -> Tuple[bool, str]:
        """
        Проверяет корректность даты
        Возвращает (успех, сообщение_об_ошибке)
        """
        if not date_str or not date_str.strip():
            return False, "Дата не может быть пустой!"
        
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True, ""
        except ValueError:
            return False, "Неверный формат даты! Используйте ГГГГ-ММ-ДД (например, 2026-05-09)"
    
    @staticmethod
    def validate_duration(duration) -> Tuple[bool, str]:
        """
        Проверяет корректность длительности
        Возвращает (успех, сообщение_об_ошибке)
        """
        try:
            dur = float(duration)
            if dur <= 0:
                return False, "Длительность должна быть положительным числом!"
            if dur > 480:  # 8 часов максимум
                return False, "Длительность не может превышать 480 минут (8 часов)!"
            return True, ""
        except (ValueError, TypeError):
            return False, "Длительность должна быть числом!"
    
    def add_training(self, date: str, training_type: str, duration: float) -> Tuple[bool, str]:
        """
        Добавляет тренировку
        Возвращает (успех, сообщение)
        """
        # Валидация
        date_valid, date_msg = self.validate_date(date)
        if not date_valid:
            return False, date_msg
        
        duration_valid, duration_msg = self.validate_duration(duration)
        if not duration_valid:
            return False, duration_msg
        
        # Проверка типа тренировки
        if training_type not in self.training_types:
            return False, f"Неверный тип тренировки! Доступные: {', '.join(self.training_types)}"
        
        # Добавляем тренировку
        training = {
            "date": date,
            "type": training_type,
            "duration": float(duration)
        }
        self.trainings.append(training)
        self.save_data()
        return True, "Тренировка успешно добавлена!"
    
    def filter_by_type(self, training_type: Optional[str] = None) -> List[Dict]:
        """Фильтрует тренировки по типу"""
        if not training_type or training_type == "Все":
            return self.trainings.copy()
        return [t for t in self.trainings if t["type"] == training_type]
    
    def filter_by_date(self, date: Optional[str] = None) -> List[Dict]:
        """Фильтрует тренировки по дате"""
        if not date:
            return self.trainings.copy()
        return [t for t in self.trainings if t["date"] == date]
    
    def filter_by_both(self, training_type: Optional[str] = None, date: Optional[str] = None) -> List[Dict]:
        """Фильтрует тренировки по типу И дате"""
        result = self.trainings.copy()
        
        if training_type and training_type != "Все":
            result = [t for t in result if t["type"] == training_type]
        
        if date:
            result = [t for t in result if t["date"] == date]
        
        return result
    
    def save_data(self):
        """Сохраняет данные в JSON"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.trainings, f, ensure_ascii=False, indent=2)
        except Exception as e:
            raise Exception(f"Ошибка сохранения: {e}")
    
    def load_data(self):
        """Загружает данные из JSON"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                self.trainings = json.load(f)
        except FileNotFoundError:
            self.trainings = []
            self.save_data()
        except json.JSONDecodeError:
            self.trainings = []
    
    def clear_all(self):
        """Очищает все тренировки"""
        self.trainings = []
        self.save_data()
    
    def delete_training(self, index: int) -> bool:
        """Удаляет тренировку по индексу"""
        if 0 <= index < len(self.trainings):
            self.trainings.pop(index)
            self.save_data()
            return True
        return False
    
    def get_statistics(self) -> Dict:
        """Возвращает статистику тренировок"""
        if not self.trainings:
            return {"total": 0, "total_minutes": 0, "by_type": {}}
        
        total_minutes = sum(t["duration"] for t in self.trainings)
        by_type = {}
        for t in self.trainings:
            by_type[t["type"]] = by_type.get(t["type"], 0) + 1
        
        return {
            "total": len(self.trainings),
            "total_minutes": round(total_minutes, 1),
            "by_type": by_type
        }
    
    def get_training_types(self) -> List[str]:
        """Возвращает список доступных типов тренировок"""
        return self.training_types.copy()
    
    def get_all_trainings(self) -> List[Dict]:
        """Возвращает все тренировки"""
        return self.trainings.copy()