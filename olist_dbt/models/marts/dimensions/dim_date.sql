SELECT DISTINCT
    DATE(order_purchase_timestamp) AS date_day,
    EXTRACT(YEAR FROM order_purchase_timestamp) AS year,
    EXTRACT(QUARTER FROM order_purchase_timestamp) AS quarter,
    EXTRACT(MONTH FROM order_purchase_timestamp) AS month,
    EXTRACT(WEEK FROM order_purchase_timestamp) AS week,
    EXTRACT(DAY FROM order_purchase_timestamp) AS day,
    FORMAT_DATE('%A', DATE(order_purchase_timestamp)) AS day_name,
    FORMAT_DATE('%B', DATE(order_purchase_timestamp)) AS month_name
FROM {{ ref('stg_orders') }}
WHERE order_purchase_timestamp IS NOT NULL
