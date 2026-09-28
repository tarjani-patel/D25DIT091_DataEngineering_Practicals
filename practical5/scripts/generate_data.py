
import pandas as pd
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)

# Dataset size
n = 50000

regions = ["North", "South", "East", "West"]
products = ["Laptop", "Mobile", "Tablet", "Headphones", "Keyboard"]

start_date = datetime(2024, 1, 1)

data = []

for i in range(n):
    date = start_date + timedelta(days=random.randint(0, 729))
    quantity = random.randint(1, 10)
    price = random.randint(500, 50000)

    data.append({
        "id": i + 1,
        "date": date.strftime("%Y-%m-%d"),
        "year": date.year,
        "month": date.month,
        "region": random.choice(regions),
        "product": random.choice(products),
        "quantity": quantity,
        "price": price,
        "sales": quantity * price
    })

df = pd.DataFrame(data)

# Create data folder if it does not exist
Path("data").mkdir(exist_ok=True)

# Save dataset
df.to_csv("data/retail_sales.csv", index=False)

print("Dataset generated successfully!")
print("Total records:", len(df))
print(df.head())
print("\nDataset saved at data/retail_sales.csv")