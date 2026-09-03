SELECT
    c.customer_id,
    c.customer_unique_id,
    c.customer_city,
    c.customer_state,

    COUNT(DISTINCT f.order_id) AS total_orders,
    COUNT(*) AS total_items_purchased,

    SUM(f.price) AS total_product_revenue,
    SUM(f.freight_value) AS total_freight_revenue,
    SUM(f.total_item_value) AS total_spend,

    AVG(f.price) AS average_item_price

FROM {{ ref('fact_order_items') }} AS f

LEFT JOIN {{ ref('fact_orders') }} AS o
    ON f.order_id = o.order_id

LEFT JOIN {{ ref('dim_customers') }} AS c
    ON o.customer_id = c.customer_id

GROUP BY
    c.customer_id,
    c.customer_unique_id,
    c.customer_city,
    c.customer_state
