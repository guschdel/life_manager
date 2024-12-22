import json
import os 

shop_data = {"currency": 0, "products": []}

current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, 'shop.json')

def save_data(data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def load_data():
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def return_products():
    data = load_data()
    products = data["products"]
    return products

def return_currency():
    data = load_data()
    currency = data["currency"]
    return currency

def add_to_currency(amount):
    data = load_data()
    data["currency"] += amount
    save_data(data)

def add_product(product_name, price):
    data = load_data()
    data["products"].append([product_name, price])
    save_data(data)


if not os.path.exists(file_path):
    save_data(shop_data)

