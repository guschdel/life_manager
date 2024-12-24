from datetime import date
import customtkinter 
import json
import os

from tasks.task_db_manager import return_tasks, create_new_task, delete_task
from shop.shop_manager import add_to_currency
from main_gui.main_gui import run_main_gui

class Task(customtkinter.CTkFrame):
    def __init__(self, master, objective, creation_date, limit_date, coin_reward):
        self.objective = objective
        self.creation_date = creation_date
        self.limit_date = limit_date    
        self.scrollable_frame = master
        self.coin_reward = coin_reward

        today = date.today()
        limit_day, limit_month, limit_year = limit_date.split()[0].split("/")
        if date(year = int(limit_year), month = int(limit_month), day = int(limit_day)) <  today:
            bordercolor = "#CC0000"
        else:
            bordercolor = "#6cff2c"

        super().__init__(master, border_width=2, border_color=bordercolor)

        self.objective_label = customtkinter.CTkLabel(self, text=objective)
        self.creation_date_label = customtkinter.CTkLabel(self, text=f"Created on: {creation_date}")
        self.limit_date_label = customtkinter.CTkLabel(self, text=f"Limit: {limit_date}")
        self.reward_label = customtkinter.CTkLabel(self, text=f"Reward: ${self.coin_reward}")
        self.complete_button = customtkinter.CTkButton(self, text="Complete task", 
                                                       command=self.delete_task_and_update)

        self.objective_label.grid(row=0, column=0, pady=(10,5), padx=10, sticky="w")
        self.creation_date_label.grid(row=1, column=0, pady=(0,10), padx=10, sticky="w")
        self.limit_date_label.grid(row=1, column=1, pady=(0,10), padx=10, sticky="w")
        self.reward_label.grid(row=0, column=1, pady= (10,5), padx=10, sticky="w")
        self.complete_button.grid(row=0, column=2, pady=10, padx=10, sticky="w", rowspan=2)

    def delete_task_and_update(self):
        delete_task(self.objective, self.creation_date, self.limit_date, self.coin_reward)
        self.scrollable_frame.gui_window.update_tasks()
        add_to_currency(self.coin_reward)
        self.add_to_task_complete_counter()

    def add_to_task_complete_counter(self):
        today = str(date.today())
        path_file = r"tasks\tasks_completed.json"
        if not os.path.exists(path_file):
            with open(path_file, "w") as file:
                json.dump({}, file)

        with open(path_file, "r") as file:
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
        with open(path_file, "w") as file:
            json.dump(data, file)

class ScrollableFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)
        self.gui_window = master
        self.columnconfigure(0, weight=1)

    def initialize_tasks(self):
        self.tasks = return_tasks()
        for i, task in enumerate(self.tasks):
            self.add_task(task, i)

    def add_task(self, task, row):
        objective = task[0]
        creation_date = task[1]
        limit_date = task[2]
        coin_reward = task[3]

        new_task = Task(self, objective, creation_date, limit_date, coin_reward)
        new_task.grid(row=row, column=0, sticky="ew", padx=5, pady=5)

class InputFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.gui_window = master 

        self.columnconfigure(1, weight=1)

        self.objective_label = customtkinter.CTkLabel(self, text="What's the objective of the task?")
        self.days_label = customtkinter.CTkLabel(self, text="How many days do you have to do it?")
        self.coin_reward_label = customtkinter.CTkLabel(self, text="How many coins does it give you?")
        self.objective_input = customtkinter.CTkEntry(self)
        self.days_input = customtkinter.CTkEntry(self)
        self.coin_reward_input = customtkinter.CTkEntry(self)
        self.input_button = customtkinter.CTkButton(self, text="Create task", command=self.input_task)
        
        self.objective_label.grid(row=0, column=0, padx=(10,0), sticky="w")
        self.days_label.grid(row=1, column=0, padx=(10,0), sticky="w")
        self.coin_reward_label.grid(row=2, column=0, padx=(10,0), sticky="w")
        self.objective_input.grid(row=0, column=1, sticky="ew", padx = 10)
        self.days_input.grid(row=1, column=1, sticky="ew", padx = 10)
        self.coin_reward_input.grid(row=2, column=1, sticky="ew", padx = 10)
        self.input_button.grid(row=1, column=2, padx=(0,10), rowspan=3)

    def input_task(self):
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
    
class LegendFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        

        self.red_square = customtkinter.CTkLabel(self, bg_color="#CC0000", text="      ")
        self.green_square = customtkinter.CTkLabel(self, bg_color="#6cff2c", text="      ")

        self.expired_label = customtkinter.CTkLabel(self, text="Expired", padx=5)
        self.on_going_label = customtkinter.CTkLabel(self, text="On going", padx=5)
        
        self.red_square.grid(row=0, column=0, sticky="w")
        self.green_square.grid(row=1, column=0, sticky="w")       

        self.expired_label.grid(row=0, column=1, sticky="w")
        self.on_going_label.grid(row=1, column=1, sticky="w") 

class GUI(customtkinter.CTk):
    def __init__(self):
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
        self.legend_frame.grid(row=1, column=1, sticky="sew", pady=(15,0), padx=10)

        self.shop_button = customtkinter.CTkButton(self, text="Go back", command=self.open_main_gui)
        self.shop_button.grid(row=2, column=1, sticky="sew", pady=15, padx=10)


    
    def update_tasks(self):
        self.scrollable_frame = ScrollableFrame(self)
        self.scrollable_frame.initialize_tasks()
        self.scrollable_frame.grid(row=0, column=0, sticky="nsew", columnspan=2)

    def open_main_gui(self):
        self.destroy()
        run_main_gui()
    

def run_tasks_gui():
    gui = GUI()
    gui.mainloop()


