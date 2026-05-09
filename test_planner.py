import unittest
import os
import json
from training_planner import TrainingPlanner

class TestTrainingPlanner(unittest.TestCase):
    
    def setUp(self):
        self.test_filename = "test_trainings.json"
        self.planner = TrainingPlanner(self.test_filename)
    
    def tearDown(self):
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)
    
    # ===== ПОЗИТИВНЫЕ ТЕСТЫ =====
    def test_add_training_positive(self):
        """Позитивный тест: добавление корректной тренировки"""
        success, message = self.planner.add_training("2026-05-09", "Бег", 30)
        self.assertTrue(success)
        self.assertEqual(len(self.planner.trainings), 1)
    
    def test_validate_correct_date(self):
        """Тест корректной даты"""
        valid, _ = self.planner.validate_date("2026-05-09")
        self.assertTrue(valid)
    
    def test_validate_positive_duration(self):
        """Тест корректной длительности"""
        valid, _ = self.planner.validate_duration(30)
        self.assertTrue(valid)
    
    def test_filter_by_type(self):
        """Тест фильтрации по типу"""
        self.planner.add_training("2026-05-09", "Бег", 30)
        self.planner.add_training("2026-05-10", "Йога", 45)
        
        filtered = self.planner.filter_by_type("Бег")
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["type"], "Бег")
    
    def test_filter_by_date(self):
        """Тест фильтрации по дате"""
        self.planner.add_training("2026-05-09", "Бег", 30)
        self.planner.add_training("2026-05-10", "Йога", 45)
        
        filtered = self.planner.filter_by_date("2026-05-09")
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["date"], "2026-05-09")
    
    def test_filter_by_both(self):
        """Тест фильтрации по типу И дате"""
        self.planner.add_training("2026-05-09", "Бег", 30)
        self.planner.add_training("2026-05-09", "Йога", 45)
        self.planner.add_training("2026-05-10", "Бег", 25)
        
        filtered = self.planner.filter_by_both("Бег", "2026-05-09")
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["type"], "Бег")
        self.assertEqual(filtered[0]["date"], "2026-05-09")
    
    # ===== НЕГАТИВНЫЕ ТЕСТЫ =====
    def test_add_training_invalid_date(self):
        """Негативный тест: неверный формат даты"""
        success, message = self.planner.add_training("09-05-2026", "Бег", 30)
        self.assertFalse(success)
        self.assertIn("формат даты", message)
    
    def test_add_training_negative_duration(self):
        """Негативный тест: отрицательная длительность"""
        success, message = self.planner.add_training("2026-05-09", "Бег", -30)
        self.assertFalse(success)
        self.assertIn("положительным", message)
    
    def test_add_training_zero_duration(self):
        """Негативный тест: нулевая длительность"""
        success, message = self.planner.add_training("2026-05-09", "Бег", 0)
        self.assertFalse(success)
        self.assertIn("положительным", message)
    
    def test_add_training_invalid_type(self):
        """Негативный тест: неверный тип тренировки"""
        success, message = self.planner.add_training("2026-05-09", "Теннис", 30)
        self.assertFalse(success)
        self.assertIn("Неверный тип", message)
    
    # ===== ГРАНИЧНЫЕ ТЕСТЫ =====
    def test_max_duration(self):
        """Граничный тест: максимальная длительность"""
        success, message = self.planner.add_training("2026-05-09", "Бег", 480)
        self.assertTrue(success)
    
    def test_exceed_max_duration(self):
        """Граничный тест: превышение максимальной длительности"""
        success, message = self.planner.add_training("2026-05-09", "Бег", 481)
        self.assertFalse(success)
        self.assertIn("превышать", message)
    
    def test_save_and_load(self):
        """Тест сохранения и загрузки JSON"""
        self.planner.add_training("2026-05-09", "Бег", 30)
        
        new_planner = TrainingPlanner(self.test_filename)
        self.assertEqual(len(new_planner.trainings), 1)
    
    def test_statistics(self):
        """Тест статистики"""
        self.planner.add_training("2026-05-09", "Бег", 30)
        self.planner.add_training("2026-05-10", "Йога", 45)
        
        stats = self.planner.get_statistics()
        self.assertEqual(stats["total"], 2)
        self.assertEqual(stats["total_minutes"], 75)
        self.assertEqual(stats["by_type"]["Бег"], 1)
        self.assertEqual(stats["by_type"]["Йога"], 1)
    
    def test_delete_training(self):
        """Тест удаления тренировки"""
        self.planner.add_training("2026-05-09", "Бег", 30)
        self.assertEqual(len(self.planner.trainings), 1)
        
        self.planner.delete_training(0)
        self.assertEqual(len(self.planner.trainings), 0)

if __name__ == "__main__":
    unittest.main()