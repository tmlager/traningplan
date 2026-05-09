#!/usr/bin/env python3
"""
Training Planner - Точка входа в приложение
"""

import tkinter as tk
from gui import TrainingPlannerApp

def main():
    root = tk.Tk()
    app = TrainingPlannerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()