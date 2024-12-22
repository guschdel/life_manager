import customtkinter

class MainGui(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("200x150")
        self.title("Life Manager")

        self.columnconfigure(0, weight=1)

        self.tasks_button = customtkinter.CTkButton(self, text="Go to tasks", command=self.open_tasks_gui)
        self.tasks_button.grid(row=0, column=0, pady=(5, 15), padx=10)

        self.shop_button = customtkinter.CTkButton(self, text="Go to shop", command=self.open_shop_gui)
        self.shop_button.grid(row=1, column=0, pady=(15, 5), padx=10)

    def open_tasks_gui(self):
        from tasks.tasks_gui import run_tasks_gui
        self.destroy()
        run_tasks_gui()

    def open_shop_gui(self):
        from shop.shop_gui import run_shop_gui
        self.destroy()
        run_shop_gui()


def run_main_gui():
    gui = MainGui()
    gui.mainloop()