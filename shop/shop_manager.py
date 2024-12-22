import json
import os 

shop_data = {"currency": 0, "products": []}

current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, 'shop.json')

def save_data(data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def load_data():
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def add_to_currency(amount):
    data = load_data()
    data["currency"] += amount
    save_data(data)

