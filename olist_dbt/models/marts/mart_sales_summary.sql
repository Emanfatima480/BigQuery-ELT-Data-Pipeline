SELECT
    f.order_date,

    COUNT(DISTINCT f.order_id) AS total_orders,
    COUNT(*) AS total_items_sold,

    SUM(f.price) AS total_product_revenue,
    SUM(f.freight_value) AS total_freight_revenue,
    SUM(f.total_item_value) AS total_sales_value,

    AVG(f.total_item_value) AS average_item_value

FROM {{ ref('fact_order_items') }} AS f

GROUP BY
    f.order_date
