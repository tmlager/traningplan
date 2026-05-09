import unittest
import os
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
        success, message = self.planner.add_training("2026-05-09", "Бег", 30)
        self.assertTrue(success)
        self.assertEqual(len(self.planner.trainings), 1)
    
    def test_validate_correct_date(self):
        valid, _ = TrainingPlanner.validate_date("2026-05-09")
        self.assertTrue(valid)
    
    def test_validate_positive_duration(self):
        valid, _ = TrainingPlanner.validate_duration(30)
        self.assertTrue(valid)
    
    def test_filter_by_type(self):
        self.planner.add_training("2026-05-09", "Бег", 30)
        self.planner.add_training("2026-05-10", "Йога", 45)
        
        filtered = self.planner.filter_by_type("Бег")
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["type"], "Бег")
    
    def test_filter_by_date(self):
        self.planner.add_training("2026-05-09", "Бег", 30)
        self.planner.add_training("2026-05-10", "Йога", 45)
        
        filtered = self.planner.filter_by_date("2026-05-09")
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["date"], "2026-05-09")
    
    def test_filter_by_both(self):
        self.planner.add_training("2026-05-09", "Бег", 30)
        self.planner.add_training("2026-05-09", "Йога", 45)
        self.planner.add_training("2026-05-10", "Бег", 25)
        
        filtered = self.planner.filter_by_both("Бег", "2026-05-09")
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["type"], "Бег")
        self.assertEqual(filtered[0]["date"], "2026-05-09")
    
    # ===== НЕГАТИВНЫЕ ТЕСТЫ =====
    def test_add_training_invalid_date(self):
        success, message = self.planner.add_training("09-05-2026", "Бег", 30)
        self.assertFalse(success)
        self.assertIn("формат даты", message)
    
    def test_add_training_empty_date(self):
        success, message = self.planner.add_training("", "Бег", 30)
        self.assertFalse(success)
    
    def test_add_training_negative_duration(self):
        success, message = self.planner.add_training("2026-05-09", "Бег", -30)
        self.assertFalse(success)
        self.assertIn("положительным", message)
    
    def test_add_training_zero_duration(self):
        success, message = self.planner.add_training("2026-05-09", "Бег", 0)
        self.assertFalse(success)
        self.assertIn("положительным", message)
    
    def test_add_training_invalid_type(self):
        success, message = self.planner.add_training("2026-05-09", "Теннис", 30)
        self.assertFalse(success)
        self.assertIn("Неверный тип", message)
    
    # ===== ГРАНИЧНЫЕ ТЕСТЫ =====
    def test_max_duration(self):
        success, message = self.planner.add_training("2026-05-09", "Бег", 480)
        self.assertTrue(success)
    
    def test_exceed_max_duration(self):
        success, message = self.planner.add_training("2026-05-09", "Бег", 481)
        self.assertFalse(success)
        self.assertIn("превышать", message)
    
    def test_save_and_load(self):
        self.planner.add_training("2026-05-09", "Бег", 30)
        
        new_planner = TrainingPlanner(self.test_filename)
        self.assertEqual(len(new_planner.trainings), 1)
    
    def test_statistics(self):
        self.planner.add_training("2026-05-09", "Бег", 30)
        self.planner.add_training("2026-05-10", "Йога", 45)
        
        stats = self.planner.get_statistics()
        self.assertEqual(stats["total"], 2)
        self.assertEqual(stats["total_minutes"], 75)
    
    def test_delete_training(self):
        self.planner.add_training("2026-05-09", "Бег", 30)
        self.assertEqual(len(self.planner.trainings), 1)
        
        self.planner.delete_training(0)
        self.assertEqual(len(self.planner.trainings), 0)

if __name__ == "__main__":
    unittest.main()