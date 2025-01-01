"""handles the shop data"""
import json
import os

shop_data = {"currency": 0, "products": []}

current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, 'shop.json')

def save_data(data) -> None:
    """Save all shop data into a json file"""
    with open(file_path, 'w', encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def load_data() -> any:
    """Get data from the json file"""
    with open(file_path, encoding="utf-8") as file:
        data = json.load(file)
    return data

def return_products() -> list:
    """Return a list of all products available"""
    data = load_data()
    products = data["products"]
    return products

def return_currency() -> int:
    """Returns the amount of money available"""
    data = load_data()
    currency = data["currency"]
    return currency

def add_to_currency(amount: int) -> None:
    """Adds monney to the bank"""
    data = load_data()
    data["currency"] += amount
    save_data(data)

def add_product(product_name: str, price: int) -> None:
    """Adds a product to the json file"""
    data = load_data()
    data["products"].append([product_name, price])
    save_data(data)

if not os.path.exists(file_path):
    save_data(shop_data)
