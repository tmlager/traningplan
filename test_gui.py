import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk
from gui import TrainingPlannerApp

class TestTrainingPlannerGUI(unittest.TestCase):
    
    def setUp(self):
        """Создаём тестовое окно"""
        self.root = tk.Tk()
        self.root.withdraw()  # Скрываем окно
        
        # Мокаем TrainingPlanner
        self.mock_planner_patch = patch('gui.TrainingPlanner')
        self.mock_planner_class = self.mock_planner_patch.start()
        self.mock_planner = MagicMock()
        self.mock_planner_class.return_value = self.mock_planner
        
        # Настройка мока
        self.mock_planner.get_training_types.return_value = ["Бег", "Йога", "Силовая"]
        self.mock_planner.get_all_trainings.return_value = []
        self.mock_planner.get_statistics.return_value = {"total": 0, "total_minutes": 0, "by_type": {}}
        
        self.app = TrainingPlannerApp(self.root)
    
    def tearDown(self):
        """Очистка"""
        self.mock_planner_patch.stop()
        self.root.destroy()
    
    def test_validate_gui_inputs_valid(self):
        """Тест валидации корректных данных"""
        self.app.date_entry.delete(0, tk.END)
        self.app.date_entry.insert(0, "2026-05-09")
        self.app.duration_entry.delete(0, tk.END)
        self.app.duration_entry.insert(0, "30")
        
        is_valid, date, t_type, duration, error = self.app.validate_gui_inputs()
        
        self.assertTrue(is_valid)
        self.assertEqual(date, "2026-05-09")
        self.assertEqual(duration, 30)
        self.assertIsNone(error)
    
    def test_validate_gui_inputs_empty_date(self):
        """Тест валидации: пустая дата"""
        self.app.date_entry.delete(0, tk.END)
        self.app.date_entry.insert(0, "")
        
        is_valid, _, _, _, error = self.app.validate_gui_inputs()
        
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
    
    def test_validate_gui_inputs_empty_duration(self):
        """Тест валидации: пустая длительность"""
        self.app.date_entry.delete(0, tk.END)
        self.app.date_entry.insert(0, "2026-05-09")
        self.app.duration_entry.delete(0, tk.END)
        self.app.duration_entry.insert(0, "")
        
        is_valid, _, _, _, error = self.app.validate_gui_inputs()
        
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
    
    def test_validate_gui_inputs_invalid_duration(self):
        """Тест валидации: нечисловая длительность"""
        self.app.date_entry.delete(0, tk.END)
        self.app.date_entry.insert(0, "2026-05-09")
        self.app.duration_entry.delete(0, tk.END)
        self.app.duration_entry.insert(0, "abc")
        
        is_valid, _, _, _, error = self.app.validate_gui_inputs()
        
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
    
    @patch('gui.messagebox')
    def test_add_training_calls_planner(self, mock_messagebox):
        """Тест: добавление тренировки вызывает метод planner"""
        self.app.date_entry.delete(0, tk.END)
        self.app.date_entry.insert(0, "2026-05-09")
        self.app.duration_entry.delete(0, tk.END)
        self.app.duration_entry.insert(0, "30")
        
        self.mock_planner.add_training.return_value = (True, "Успех")
        
        self.app.add_training()
        
        self.mock_planner.add_training.assert_called_once_with("2026-05-09", "Бег", 30.0)
    
    @patch('gui.messagebox')
    def test_add_training_shows_error_on_invalid_input(self, mock_messagebox):
        """Тест: при неверном вводе показывается ошибка"""
        self.app.date_entry.delete(0, tk.END)
        self.app.date_entry.insert(0, "invalid-date")
        self.app.duration_entry.delete(0, tk.END)
        self.app.duration_entry.insert(0, "30")
        
        self.app.add_training()
        
        # Проверяем, что метод planner не вызывался
        self.mock_planner.add_training.assert_not_called()
        mock_messagebox.showerror.assert_called()

if __name__ == "__main__":
    unittest.main()