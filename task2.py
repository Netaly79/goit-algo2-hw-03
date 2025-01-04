import csv
from BTrees.OOBTree import OOBTree
from timeit import timeit

def load_data(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = []
        for row in reader:
            item = {
                "ID": int(row["ID"]),
                "Name": row["Name"],
                "Category": row["Category"],
                "Price": float(row["Price"])
            }
            data.append(item)
        return data

def add_item_to_tree(tree, item):
    tree[item["ID"]] = {
        "Name": item["Name"],
        "Category": item["Category"],
        "Price": item["Price"]
    }

def add_item_to_dict(dictionary, item):
    dictionary[item["ID"]] = {
        "Name": item["Name"],
        "Category": item["Category"],
        "Price": item["Price"]
    }

def range_query_tree(tree, min_price, max_price):
    return [
      value for key, value in tree.items(min_price, max_price)
        if min_price <= value["Price"] <= max_price
    ]

def range_query_dict(dictionary, min_price, max_price):
    return [
        value for value in dictionary.values() 
        if min_price <= value["Price"] <= max_price
    ]


if __name__ == "__main__":
    file_path = "generated_items_data.csv"
    items = load_data(file_path)

    tree = OOBTree()
    dictionary = {}


    for item in items:
        add_item_to_tree(tree, item)
        add_item_to_dict(dictionary, item)


    min_price = 100
    max_price = 200
    iterations = 100

    tree_time = timeit(
        lambda: range_query_tree(tree, min_price, max_price), 
        number=iterations
    )

    dict_time = timeit(
        lambda: range_query_dict(dictionary, min_price, max_price), 
        number=iterations
    )

    print(f"Total range_query time for OOBTree: {tree_time:.6f} seconds")
    print(f"Total range_query time for Dict: {dict_time:.6f} seconds")
