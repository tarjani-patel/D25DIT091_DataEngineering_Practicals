import pandas as pd
import random

random.seed(42)

products = [
    ("Laptop", "Electronics"),
    ("Mobile Phone", "Electronics"),
    ("Headphones", "Electronics"),
    ("T-Shirt", "Clothing"),
    ("Jeans", "Clothing"),
    ("Shoes", "Clothing"),
    ("Rice", "Grocery"),
    ("Oil", "Grocery"),
    ("Biscuits", "Grocery"),
    ("Coffee", "Beverages"),
    ("Juice", "Beverages"),
    ("Chips", "Grocery")
]

store_codes = ["S001", "S002", "S003", "OLD01", "OLD02"]

rows = []

for i in range(1, 100001):
    product, category = random.choice(products)
    store = random.choice(store_codes)

    quantity = random.randint(1, 20)
    unit_price = random.choice([99, 149, 199, 249, 499, 999, 1499, 2499, 4999])

    # Deliberately introduce inconsistent spaces
    order_id = f" ORD{i:06d} " if i % 3 == 0 else f"ORD{i:06d}"
    store_value = f" {store} " if i % 4 == 0 else store
    product_value = f" {product} " if i % 5 == 0 else product
    category_value = f" {category} " if i % 6 == 0 else category

    # Store numeric values as strings
    quantity_value = f" {quantity} "
    price_value = f" {unit_price} "

    rows.append([
        order_id,
        store_value,
        product_value,
        category_value,
        quantity_value,
        price_value
    ])

df = pd.DataFrame(
    rows,
    columns=[
        "order_id",
        "store_code",
        "product",
        "category",
        "quantity",
        "unit_price"
    ]
)

df.to_csv("data/retail_sales_raw.csv", index=False)

print("Dataset created successfully!")
print("Rows:", len(df))
print("Columns:", len(df.columns))
print("\nFirst 5 records:")
print(df.head())