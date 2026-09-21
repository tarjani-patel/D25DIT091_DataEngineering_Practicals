import duckdb
import os
import pandas as pd

DATABASE_FILE = "warehouse/retail.duckdb"
SOURCE_FILE = "data/retail_sales_raw.csv"

print("=" * 70)
print("RESOURCE AND OUTPUT ANALYSIS")
print("=" * 70)

# ---------------------------------------------------------
# FILE SIZE ANALYSIS
# ---------------------------------------------------------

raw_size = os.path.getsize(SOURCE_FILE)

print("\n1. SOURCE DATA SIZE")
print(f"Raw CSV size: {raw_size / (1024 * 1024):.4f} MB")


# ---------------------------------------------------------
# DATABASE ANALYSIS
# ---------------------------------------------------------

con = duckdb.connect(DATABASE_FILE)

print("\n2. DATABASE TABLE SIZES")

tables = [
    "retail_sales_staging",
    "retail_sales_etl",
    "retail_sales_elt"
]

for table in tables:

    count = con.execute(
        f"SELECT COUNT(*) FROM {table}"
    ).fetchone()[0]

    print(f"{table}: {count:,} rows")


# ---------------------------------------------------------
# ETL VS ELT DATA VALIDATION
# ---------------------------------------------------------

print("\n3. ETL VS ELT VALIDATION")

etl_count = con.execute("""
    SELECT COUNT(*)
    FROM retail_sales_etl
""").fetchone()[0]

elt_count = con.execute("""
    SELECT COUNT(*)
    FROM retail_sales_elt
""").fetchone()[0]

etl_total = con.execute("""
    SELECT ROUND(SUM(total_amount), 2)
    FROM retail_sales_etl
""").fetchone()[0]

elt_total = con.execute("""
    SELECT ROUND(SUM(total_amount), 2)
    FROM retail_sales_elt
""").fetchone()[0]

print(f"ETL row count : {etl_count:,}")
print(f"ELT row count : {elt_count:,}")

print(f"ETL total sales: {etl_total:,.2f}")
print(f"ELT total sales: {elt_total:,.2f}")

if etl_count == elt_count and etl_total == elt_total:
    print("RESULT: ETL and ELT outputs are equivalent.")
else:
    print("RESULT: Outputs differ.")


# ---------------------------------------------------------
# RESOURCE ARCHITECTURE
# ---------------------------------------------------------

print("\n4. RESOURCE ARCHITECTURE")

print("""
ETL:
Source CSV
    |
    v
Python/Pandas application compute
    |
    | Transformed records
    v
DuckDB warehouse

ELT:
Source CSV
    |
    | Raw records
    v
DuckDB staging
    |
    | SQL transformation
    v
DuckDB final table
""")


# ---------------------------------------------------------
# NETWORK / COMPUTE INTERPRETATION
# ---------------------------------------------------------

print("5. NETWORK AND COMPUTE INTERPRETATION")

print("""
ETL:
- Transformation is performed in the application layer.
- Application CPU and memory are used for transformation.
- In a distributed system, transformed data must then be sent
  from the application compute layer to the warehouse.
- Intermediate transformed data is therefore part of the
  application-to-warehouse data movement.

ELT:
- Raw data is loaded into the warehouse first.
- Transformation is performed by the database/warehouse engine.
- Application compute performs less transformation work.
- In a cloud architecture, this can reduce movement of
  intermediate transformed datasets between application
  compute and warehouse systems.

Important:
This experiment runs locally, so it does not measure actual
network bandwidth or cloud transfer charges. It demonstrates
the architectural difference in where computation occurs.
""")


# ---------------------------------------------------------
# FINAL SUMMARY
# ---------------------------------------------------------

print("=" * 70)
print("RESOURCE ANALYSIS COMPLETED")
print("=" * 70)

con.close()