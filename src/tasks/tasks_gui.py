"""Creates the GUI to handle the tasks"""


import json
import os
from datetime import date

import customtkinter as ctk

from ..shop.shop_manager import add_to_currency
from .task_db_manager import TaskElement, create_new_task, delete_task, return_tasks

# from main_gui.main_gui import run_main_gui


class Task(ctk.CTkFrame):
    """representation of a single task"""

    def __init__(self, master, task: TaskElement) -> None:
        self.task = task
        self.scrollable_frame = master

        today = date.today()
        limit_day, limit_month, limit_year = task.time_limit.split()[0].split("/")
        if date(year=int(limit_year), month=int(limit_month), day=int(limit_day)) < today:
            bordercolor = "#CC0000"
        else:
            bordercolor = "#6cff2c"

        super().__init__(master, border_width=2, border_color=bordercolor)

        self.objective_label = ctk.CTkLabel(self, text=task.objective)
        self.creation_date_label = ctk.CTkLabel(self, text=f"Created on: {self.task.creation_date}")
        self.limit_date_label = ctk.CTkLabel(self, text=f"Limit: {self.task.time_limit}")
        self.reward_label = ctk.CTkLabel(self, text=f"Reward: ${self.task.coins}")
        self.complete_button = ctk.CTkButton(self, text="Complete task", command=self.delete_task_and_update)

        self.objective_label.grid(row=0, column=0, pady=(10, 5), padx=10, sticky="w")
        self.creation_date_label.grid(row=1, column=0, pady=(0, 10), padx=10, sticky="w")
        self.limit_date_label.grid(row=1, column=1, pady=(0, 10), padx=10, sticky="w")
        self.reward_label.grid(row=0, column=1, pady=(10, 5), padx=10, sticky="w")
        self.complete_button.grid(row=0, column=2, pady=10, padx=10, sticky="w", rowspan=2)

    def delete_task_and_update(self) -> None:
        """Deletes a task and updates the tasks completed"""
        delete_task(self.task)
        self.scrollable_frame.gui_window.update_tasks()
        add_to_currency(self.task.coins)
        self.add_to_task_complete_counter()

    def add_to_task_complete_counter(self) -> None:
        """Adding another task to the counter"""
        today = str(date.today())
        # path_file = r"tasks\tasks_completed.json"
        current_dir = os.path.dirname(__file__)
        path_file = os.path.join(current_dir, "tasks_completed.json")
        if not os.path.exists(path_file):
            with open(path_file, "w", encoding="utf-8") as file:
                json.dump({}, file)

        with open(path_file, encoding="utf-8") as file:
            try:
                data = json.load(file)
            except FileNotFoundError:
                data = {}
            except json.JSONDecodeError:
                data = {}
            if today in data:
                data[today] += 1
            else:
                data[today] = 1
        with open(path_file, "w", encoding="utf-8") as file:
            json.dump(data, file)


class ScrollableFrame(ctk.CTkScrollableFrame):
    """Frame that holds all the active tasks"""

    def __init__(self, master) -> None:
        super().__init__(master)
        self.gui_window = master
        self.columnconfigure(0, weight=1)

    def initialize_tasks(self) -> None:
        """Get the tasks from the database"""
        self.tasks = return_tasks()
        for i, task in enumerate(self.tasks):
            self.add_task(task, i)

    def add_task(self, task: TaskElement, row: int) -> None:
        """Add a new tasks to the list?"""
        new_task = Task(self, task)
        new_task.grid(row=row, column=0, sticky="ew", padx=5, pady=5)


class InputFrame(ctk.CTkFrame):
    """Frame to input new tasks"""

    def __init__(self, master):
        super().__init__(master)
        self.gui_window = master

        self.columnconfigure(1, weight=1)

        self.objective_label = ctk.CTkLabel(self, text="What's the objective of the task?")
        self.days_label = ctk.CTkLabel(self, text="How many days do you have to do it?")
        self.coin_reward_label = ctk.CTkLabel(self, text="How many coins does it give you?")
        self.objective_input = ctk.CTkEntry(self)
        self.days_input = ctk.CTkEntry(self)
        self.coin_reward_input = ctk.CTkEntry(self)
        self.input_button = ctk.CTkButton(self, text="Create task", command=self.input_task)

        self.objective_label.grid(row=0, column=0, padx=(10, 0), sticky="w")
        self.days_label.grid(row=1, column=0, padx=(10, 0), sticky="w")
        self.coin_reward_label.grid(row=2, column=0, padx=(10, 0), sticky="w")
        self.objective_input.grid(row=0, column=1, sticky="ew", padx=10)
        self.days_input.grid(row=1, column=1, sticky="ew", padx=10)
        self.coin_reward_input.grid(row=2, column=1, sticky="ew", padx=10)
        self.input_button.grid(row=1, column=2, padx=(0, 10), rowspan=3)

    def input_task(self):
        """Callback function to insert the specified task"""
        objective = self.objective_input.get().strip()
        days = self.days_input.get().strip()
        coin_reward = self.coin_reward_input.get().strip()

        if not coin_reward:
            coin_reward = 0
        try:
            days = int(days)
        except ValueError:
            days = None

        if objective and days:
            create_new_task(objective, days, coin_reward)
            self.gui_window.update_tasks()


class LegendFrame(ctk.CTkFrame):
    """Represents the legend in the lower right corner"""

    def __init__(self, master) -> None:
        super().__init__(master)

        self.red_square = ctk.CTkLabel(self, bg_color="#CC0000", text="      ")
        self.green_square = ctk.CTkLabel(self, bg_color="#6cff2c", text="      ")

        self.expired_label = ctk.CTkLabel(self, text="Expired", padx=5)
        self.on_going_label = ctk.CTkLabel(self, text="On going", padx=5)

        self.red_square.grid(row=0, column=0, sticky="w")
        self.green_square.grid(row=1, column=0, sticky="w")

        self.expired_label.grid(row=0, column=1, sticky="w")
        self.on_going_label.grid(row=1, column=1, sticky="w")


class GUI(ctk.CTk):
    """the main window for the tasks"""

    def __init__(self) -> None:
        super().__init__()

        self.geometry("800x600")
        self.title("Task manager")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.scrollable_frame = ScrollableFrame(self)

        self.update_tasks()

        self.input_frame = InputFrame(self)
        self.input_frame.grid(row=1, column=0, pady=15, padx=10, sticky="nsew", rowspan=2)

        self.legend_frame = LegendFrame(self)
        self.legend_frame.grid(row=1, column=1, sticky="sew", pady=(15, 0), padx=10)

        self.shop_button = ctk.CTkButton(self, text="Go back", command=self.open_main_gui)
        self.shop_button.grid(row=2, column=1, sticky="sew", pady=15, padx=10)

    def update_tasks(self) -> None:
        """Updates the list of tasks"""
        self.scrollable_frame = ScrollableFrame(self)
        self.scrollable_frame.initialize_tasks()
        self.scrollable_frame.grid(row=0, column=0, sticky="nsew", columnspan=2)

    def open_main_gui(self) -> None:
        """Returns to the main window"""
        self.destroy()
        # run_main_gui()


def run_tasks_gui():
    """Shows the tasks window"""
    gui = GUI()
    gui.mainloop()
