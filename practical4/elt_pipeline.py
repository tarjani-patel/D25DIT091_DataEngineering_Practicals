import duckdb
import time
import os

SOURCE_FILE = "data/retail_sales_raw.csv"
DATABASE_FILE = "warehouse/retail.duckdb"

print("=" * 60)
print("ELT PIPELINE")
print("=" * 60)

os.makedirs("warehouse", exist_ok=True)

con = duckdb.connect(DATABASE_FILE)

# ---------------------------------------------------------
# EXTRACT + LOAD
# ---------------------------------------------------------
load_start = time.perf_counter()

con.execute("DROP TABLE IF EXISTS retail_sales_staging")

con.execute("""
    CREATE TABLE retail_sales_staging AS
    SELECT *
    FROM read_csv_auto(?)
""", [SOURCE_FILE])

load_time = time.perf_counter() - load_start

staging_count = con.execute("""
    SELECT COUNT(*)
    FROM retail_sales_staging
""").fetchone()[0]

print("\nEXTRACT + LOAD")
print(f"Raw rows loaded into staging: {staging_count}")
print(f"Staging load time: {load_time:.4f} seconds")


# ---------------------------------------------------------
# TRANSFORM INSIDE DUCKDB
# ---------------------------------------------------------
transform_start = time.perf_counter()

con.execute("DROP TABLE IF EXISTS retail_sales_elt")

con.execute("""
    CREATE TABLE retail_sales_elt AS

    SELECT
        TRIM(CAST(order_id AS VARCHAR)) AS order_id,

        CASE
            WHEN TRIM(CAST(store_code AS VARCHAR)) = 'OLD01'
                THEN 'S001'
            WHEN TRIM(CAST(store_code AS VARCHAR)) = 'OLD02'
                THEN 'S002'
            ELSE TRIM(CAST(store_code AS VARCHAR))
        END AS store_code,

        TRIM(CAST(product AS VARCHAR)) AS product,

        TRIM(CAST(category AS VARCHAR)) AS category,

        CAST(quantity AS INTEGER) AS quantity,

        CAST(unit_price AS DOUBLE) AS unit_price,

        CAST(quantity AS INTEGER)
            * CAST(unit_price AS DOUBLE) AS total_amount,

        'retail_sales_raw.csv' AS source_system,

        TRUE AS elt_processed

    FROM retail_sales_staging
""")

transform_time = time.perf_counter() - transform_start

print("\nTRANSFORM")
print("Whitespace removed using SQL")
print("Legacy store codes standardized using CASE")
print("Numeric values converted using CAST")
print("Product and category values cleaned using TRIM")
print("Total amount calculated inside DuckDB")
print("Data lineage columns added")
print(f"SQL transformation time: {transform_time:.4f} seconds")


# ---------------------------------------------------------
# VALIDATION
# ---------------------------------------------------------
result = con.execute("""
    SELECT
        COUNT(*) AS total_rows,
        SUM(total_amount) AS total_sales
    FROM retail_sales_elt
""").fetchone()

print("\nVALIDATION")
print(f"Rows in final ELT table: {result[0]}")
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
    FROM retail_sales_elt
    LIMIT 5
""").fetchdf()

print(sample.to_string(index=False))


# ---------------------------------------------------------
# PERFORMANCE SUMMARY
# ---------------------------------------------------------
total_time = load_time + transform_time

print("\n" + "=" * 60)
print("ELT PERFORMANCE SUMMARY")
print("=" * 60)
print(f"Load time       : {load_time:.4f} seconds")
print(f"Transform time  : {transform_time:.4f} seconds")
print(f"Total ELT time  : {total_time:.4f} seconds")

con.close()

print("\nELT PIPELINE COMPLETED SUCCESSFULLY!")