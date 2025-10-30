"""
inventory_system.py: Improved after static code analysis.

Fixes:
- Mutable default arguments
- Bare except
- Input validation
- Dangerous eval
- Coding style (PEP8: docstrings, line length, naming, blank lines)
- Resource management and encoding
"""

import json
from datetime import datetime


# Global variable to store inventory stock data
stock_data = {}


def add_item(item="default", qty=0, logs=None):
    """
    Add quantity of an item to stock_data with validation and logging.
    """
    if logs is None:
        logs = []
    if not isinstance(item, str) or not isinstance(qty, int):
        print("Invalid item type or quantity type")
        return
    if not item:
        return
    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append(f"{datetime.now()}: Added {qty} of {item}")


def remove_item(item, qty):
    """
    Remove quantity from item in stock_data, remove item if depleted.
    """
    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
    except KeyError:
        print(f"Item '{item}' not found in inventory.")


def get_qty(item):
    """
    Return quantity of specified item.
    """
    return stock_data.get(item, 0)


def load_data(file="inventory.json"):
    """
    Load inventory data from JSON file.
    """
    global stock_data
    try:
        with open(file, "r", encoding="utf-8") as f:
            stock_data = json.loads(f.read())
    except FileNotFoundError:
        print(f"File {file} not found. Starting with empty inventory.")
        stock_data = {}
    except json.JSONDecodeError:
        print(f"Error decoding JSON in {file}. Starting with empty inventory.")
        stock_data = {}


def save_data(file="inventory.json"):
    """
    Save inventory data to JSON file.
    """
    with open(file, "w", encoding="utf-8") as f:
        f.write(json.dumps(stock_data))


def print_data():
    """
    Print inventory report.
    """
    print("Items Report")
    for i in stock_data:
        print(i, "->", stock_data[i])


def check_low_items(threshold=5):
    """
    Return list of items with quantity below threshold.
    """
    result = []
    for i in stock_data:
        if stock_data[i] < threshold:
            result.append(i)
    return result


def main():
    """
    Demonstrate inventory system usage.
    """
    add_item("apple", 10)
    add_item("banana", -2)
    add_item(123, "ten")  # invalid types, now safely ignored
    remove_item("apple", 3)
    remove_item("orange", 1)
    print("Apple stock:", get_qty("apple"))
    print("Low items:", check_low_items())
    save_data()
    load_data()
    print_data()
    print("Eval-unsafe code removed for security.")


if __name__ == "__main__":
    main()