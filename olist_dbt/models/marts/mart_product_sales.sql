SELECT
    p.product_id,
    p.product_category_name,
    p.product_category_name_english,

    COUNT(DISTINCT f.order_id) AS total_orders,
    COUNT(*) AS total_items_sold,

    SUM(f.price) AS total_product_revenue,
    SUM(f.freight_value) AS total_freight_revenue,
    SUM(f.total_item_value) AS total_sales_value,

    AVG(f.price) AS average_item_price

FROM {{ ref('fact_order_items') }} AS f

LEFT JOIN {{ ref('dim_products') }} AS p
    ON f.product_id = p.product_id

GROUP BY
    p.product_id,
    p.product_category_name,
    p.product_category_name_english
