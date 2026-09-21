import pandas as pd
import duckdb
import time
import os

SOURCE_FILE = "data/retail_sales_raw.csv"
DATABASE_FILE = "warehouse/retail.duckdb"

print("=" * 60)
print("ETL PIPELINE")
print("=" * 60)

# ---------------------------------------------------------
# EXTRACT
# ---------------------------------------------------------
extract_start = time.perf_counter()

df = pd.read_csv(SOURCE_FILE)

extract_time = time.perf_counter() - extract_start

print(f"\nEXTRACT")
print(f"Rows extracted: {len(df)}")
print(f"Columns extracted: {len(df.columns)}")
print(f"Extraction time: {extract_time:.4f} seconds")


# ---------------------------------------------------------
# TRANSFORM
# ---------------------------------------------------------
transform_start = time.perf_counter()

# Remove leading/trailing spaces from text columns
text_columns = ["order_id", "store_code", "product", "category"]

for column in text_columns:
    df[column] = df[column].astype(str).str.strip()

# Standardize legacy store codes
store_mapping = {
    "OLD01": "S001",
    "OLD02": "S002"
}

df["store_code"] = df["store_code"].replace(store_mapping)

# Convert numeric columns from strings to numbers
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")

# Standardize category and product text
df["category"] = df["category"].str.title()
df["product"] = df["product"].str.title()

# Calculate total sales amount
df["total_amount"] = df["quantity"] * df["unit_price"]

# Add data lineage information
df["source_system"] = "retail_sales_raw.csv"
df["etl_processed"] = True

transform_time = time.perf_counter() - transform_start

print(f"\nTRANSFORM")
print("Whitespace removed")
print("Legacy store codes standardized")
print("Numeric values converted")
print("Product/category values standardized")
print("Total amount calculated")
print("Data lineage columns added")
print(f"Transformation time: {transform_time:.4f} seconds")


# ---------------------------------------------------------
# LOAD
# ---------------------------------------------------------
load_start = time.perf_counter()

os.makedirs("warehouse", exist_ok=True)

con = duckdb.connect(DATABASE_FILE)

con.execute("DROP TABLE IF EXISTS retail_sales_etl")

con.register("pandas_data", df)

con.execute("""
    CREATE TABLE retail_sales_etl AS
    SELECT *
    FROM pandas_data
""")

con.unregister("pandas_data")

load_time = time.perf_counter() - load_start

print(f"\nLOAD")
print("Data loaded into DuckDB table: retail_sales_etl")
print(f"Loading time: {load_time:.4f} seconds")


# ---------------------------------------------------------
# VALIDATION
# ---------------------------------------------------------
result = con.execute("""
    SELECT
        COUNT(*) AS total_rows,
        SUM(total_amount) AS total_sales
    FROM retail_sales_etl
""").fetchone()

print("\nVALIDATION")
print(f"Rows in DuckDB: {result[0]}")
print(f"Total sales amount: {result[1]:,.2f}")


# ---------------------------------------------------------
# SAMPLE OUTPUT
# ---------------------------------------------------------
print("\nSAMPLE TRANSFORMED DATA")

sample = con.execute("""
    SELECT
        order_id,
        store_code,
        product,
        category,
        quantity,
        unit_price,
        total_amount
    FROM retail_sales_etl
    LIMIT 5
""").fetchdf()

print(sample.to_string(index=False))


# ---------------------------------------------------------
# PERFORMANCE SUMMARY
# ---------------------------------------------------------
total_time = extract_time + transform_time + load_time

print("\n" + "=" * 60)
print("ETL PERFORMANCE SUMMARY")
print("=" * 60)
print(f"Extract time    : {extract_time:.4f} seconds")
print(f"Transform time  : {transform_time:.4f} seconds")
print(f"Load time       : {load_time:.4f} seconds")
print(f"Total ETL time  : {total_time:.4f} seconds")

con.close()

print("\nETL PIPELINE COMPLETED SUCCESSFULLY!")