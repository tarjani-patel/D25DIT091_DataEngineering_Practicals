import duckdb
import time

DATABASE_FILE = "warehouse/retail.duckdb"

print("=" * 70)
print("DATA LINEAGE AND TRANSFORMATION RECOVERY")
print("=" * 70)

con = duckdb.connect(DATABASE_FILE)

# ---------------------------------------------------------
# CHECK RAW STAGING DATA
# ---------------------------------------------------------
print("\n1. RAW STAGING DATA")

staging_count = con.execute("""
    SELECT COUNT(*)
    FROM retail_sales_staging
""").fetchone()[0]

print(f"Rows preserved in staging: {staging_count}")


# ---------------------------------------------------------
# CHECK TRANSFORMED DATA
# ---------------------------------------------------------
print("\n2. TRANSFORMED DATA")

etl_count = con.execute("""
    SELECT COUNT(*)
    FROM retail_sales_etl
""").fetchone()[0]

elt_count = con.execute("""
    SELECT COUNT(*)
    FROM retail_sales_elt
""").fetchone()[0]

print(f"Rows in ETL table: {etl_count}")
print(f"Rows in ELT table: {elt_count}")


# ---------------------------------------------------------
# CHECK DATA LINEAGE
# ---------------------------------------------------------
print("\n3. DATA LINEAGE")

lineage = con.execute("""
    SELECT
        source_system,
        elt_processed,
        COUNT(*) AS records
    FROM retail_sales_elt
    GROUP BY source_system, elt_processed
""").fetchdf()

print(lineage.to_string(index=False))


# ---------------------------------------------------------
# SAMPLE RAW DATA
# ---------------------------------------------------------
print("\n4. RAW DATA FROM STAGING")

raw_sample = con.execute("""
    SELECT
        order_id,
        store_code,
        product,
        category,
        quantity,
        unit_price
    FROM retail_sales_staging
    LIMIT 3
""").fetchdf()

print(raw_sample.to_string(index=False))


# ---------------------------------------------------------
# SAMPLE TRANSFORMED DATA
# ---------------------------------------------------------
print("\n5. TRANSFORMED DATA")

transformed_sample = con.execute("""
    SELECT
        order_id,
        store_code,
        product,
        category,
        quantity,
        unit_price,
        total_amount
    FROM retail_sales_elt
    LIMIT 3
""").fetchdf()

print(transformed_sample.to_string(index=False))


# ---------------------------------------------------------
# SIMULATE A TRANSFORMATION BUG
# ---------------------------------------------------------
print("\n6. SIMULATING TRANSFORMATION BUG")

try:

    con.execute("DROP TABLE IF EXISTS broken_transformation")

    con.execute("""
        CREATE TABLE broken_transformation AS

        SELECT
            TRIM(CAST(order_id AS VARCHAR)) AS order_id,
            CAST(category AS INTEGER) AS category
        FROM retail_sales_staging
    """)

    print("Unexpectedly succeeded.")

except Exception as error:

    print("Transformation failed as expected.")
    print("Reason: incorrect data type conversion detected.")


# ---------------------------------------------------------
# RECOVERY FROM BUG
# ---------------------------------------------------------
print("\n7. RECOVERING FROM TRANSFORMATION BUG")

recovery_start = time.perf_counter()

con.execute("DROP TABLE IF EXISTS recovered_retail_sales")

con.execute("""
    CREATE TABLE recovered_retail_sales AS

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

        TRUE AS recovered_after_fix

    FROM retail_sales_staging
""")

recovery_time = time.perf_counter() - recovery_start

recovered_count = con.execute("""
    SELECT COUNT(*)
    FROM recovered_retail_sales
""").fetchone()[0]

print(f"Recovery completed in: {recovery_time:.4f} seconds")
print(f"Rows recovered: {recovered_count}")


# ---------------------------------------------------------
# FINAL VALIDATION
# ---------------------------------------------------------
print("\n8. FINAL VALIDATION")

if recovered_count == staging_count:
    print("SUCCESS: All raw records were recovered.")
else:
    print("WARNING: Record count mismatch.")

print("\nThe original staging data remained available,")
print("so the transformation could be corrected and rerun")
print("without re-extracting the source CSV.")

con.close()

print("\n" + "=" * 70)
print("DATA LINEAGE AND RECOVERY TEST COMPLETED!")
print("=" * 70)