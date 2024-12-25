"""Creates the main GUI for the application"""
import json
from os import path
import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tasks.tasks_gui import run_tasks_gui
from shop.shop_gui import run_shop_gui

class MainGui(ctk.CTk):
    """The main GUI class"""
    def __init__(self) -> None:
        super().__init__()

        self.geometry("800x600")
        self.title("Life Manager")

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.tasks_button = ctk.CTkButton(self,
                                          text="Go to tasks",
                                          command=self.open_tasks_gui)
        self.tasks_button.grid(row=1,
                               column=0,
                               pady=15,
                               padx=10)

        self.shop_button = ctk.CTkButton(self,
                                         text="Go to shop",
                                         command=self.open_shop_gui)
        self.shop_button.grid(row=1,
                              column=1,
                              pady=15,
                              padx=10)

        self.graph_frame = ctk.CTkFrame(self,
                                        border_width=2,
                                        border_color="#101049")
        self.graph_frame.grid(row=0,
                              column=0,
                              sticky="nsew",
                              padx=10,
                              pady=10,
                              columnspan=2)
        self.plot_graph()

    def open_tasks_gui(self) -> None:
        """Opens the GUI to manage tasks"""
        # self.destroy()
        run_tasks_gui()
        self.plot_graph()

    def open_shop_gui(self) -> None:
        """Opens the shop GUI"""
        # self.destroy()
        run_shop_gui()

    def plot_graph(self) -> None:
        """Plots the amount of tasks completed in the main window"""
        # file_path = r"tasks\tasks_completed.json"
        file_path = path.join("tasks", "tasks_completed.json")
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except json.JSONDecodeError:
            print("The file is empty")
            return
        except FileNotFoundError:
            print("The file does not exists yet")
            return

        dates = list(data.keys())
        counts = list(data.values())

        fig = Figure(figsize=(6, 6), dpi=100)
        ax = fig.add_subplot(111)
        ax.bar(dates, counts, color='skyblue', edgecolor='black')
        ax.set_title("Tasks Completed Over Time", fontsize=16)
        ax.set_xlabel("Date", fontsize=14)
        ax.set_ylabel("Number of Tasks Completed", fontsize=14)
        ax.tick_params(axis='x', labelrotation=45)

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)


def run_main_gui() -> None:
    """Runs the main GUI"""
    gui = MainGui()
    gui.mainloop()
