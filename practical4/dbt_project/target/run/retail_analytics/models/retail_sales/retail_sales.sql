
    

    create  table
      "retail"."main"."retail_sales__dbt_tmp"
  
    
    as (
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

    TRUE AS dbt_processed

FROM retail_sales_staging
    );
    
  