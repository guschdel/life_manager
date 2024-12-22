import customtkinter 
import os 
import sys

from shop_manager import add_to_currency, add_product, return_products, return_currency

class Product(customtkinter.CTkFrame):
    def __init__(self, master, product_name, price):
        super().__init__(master)

        self.scrollable_frame = master
        self.product_name = product_name
        self.price = price

        self.product_name_label = customtkinter.CTkLabel(self, text=product_name)
        self.price_label = customtkinter.CTkLabel(self, text=f"${price}")
        self.buy_button = customtkinter.CTkButton(self, text="Buy", command=self._buy_product)

        self.product_name_label.grid(row=0, column=0, pady=(10,5), padx=10, sticky="w")
        self.price_label.grid(row=1, column=0, pady=(0,10), padx=10)
        self.buy_button.grid(row=0, column=1, pady=(10,5), padx=10, sticky="w", rowspan=2)

    def _buy_product(self):
        currency = return_currency()
        if currency >= self.price:
            print("You bought one:", self.product_name)
            add_to_currency(-self.price)
            self.scrollable_frame.gui_window.money_frame.update_money_label()
        else:
            print("Not enough currency")

class ScrollableFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)
        self.gui_window = master
        self.columnconfigure(0, weight=1)
        self.initialize_products()

    def initialize_products(self):
        self.products = return_products()
        for i, product in enumerate(self.products):
            self.add_product(product, i)

    def add_product(self, product, row):
        product_name = product[0]
        price = product[1]

        new_product = Product(self, product_name, price)
        new_product.grid(row=row, column=0, sticky="ew", padx=5, pady=5)

class MoneyFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.label = customtkinter.CTkLabel(self, text = "You have: ")
        self.money_amount = customtkinter.CTkLabel(self, text = f"${return_currency()}")
    
        self.label.grid(row = 0, column = 0, padx = 10)
        self.money_amount.grid(row = 1, column = 0, padx = 10)


    def update_money_label(self):
        self.money_amount = customtkinter.CTkLabel(self, text = f"${return_currency()}")
        self.money_amount.grid(row = 1, column = 0, padx = 10)

class InputFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.gui_window = master 

        self.columnconfigure(1, weight=1)

        self.product_label = customtkinter.CTkLabel(self, text="What's the product?")
        self.price_label = customtkinter.CTkLabel(self, text="How much does it cost?")
        self.product_input = customtkinter.CTkEntry(self)
        self.price_input = customtkinter.CTkEntry(self)
        self.input_button = customtkinter.CTkButton(self, text="Create task", command=self.create_product)
        
        self.product_label.grid(row=0, column=0, padx=(10,0), sticky="w")
        self.price_label.grid(row=1, column=0, padx=(10,0), sticky="w")
        self.product_input.grid(row=0, column=1, sticky="ew", padx = 10)
        self.price_input.grid(row=1, column=1, sticky="ew", padx = 10)
        self.input_button.grid(row=1, column=2, padx=(0,10))

    def create_product(self):
        product = self.product_input.get().strip()
        price = self.price_input.get().strip()
        try:
            price = int(price)
        except:
            price = None

        if product and price:
            add_product(product, price)
            self.gui_window.update_products()
    

class GUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("800x600")
        self.title("Task manager")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.scrollable_frame = ScrollableFrame(self)

        self.update_products()

        self.input_frame = InputFrame(self)
        self.input_frame.grid(row=1, column=0, pady=15, padx=10, sticky="nsew")

        self.money_frame = MoneyFrame(self)
        self.money_frame.grid(row=1, column=1, sticky="sew", pady=15, padx=10)
    
    def update_products(self):
            self.scrollable_frame = ScrollableFrame(self)
            self.scrollable_frame.grid(row=0, column=0, sticky="nsew", columnspan=2)


def run_shop_gui():
    gui = GUI()
    gui.mainloop()

run_shop_gui()