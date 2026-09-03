SELECT
    oi.order_id,
    oi.order_item_id,
    oi.product_id,
    oi.seller_id,

    DATE(o.order_purchase_timestamp) AS order_date,

    oi.shipping_limit_date,
    oi.price,
    oi.freight_value,

    oi.price + oi.freight_value AS total_item_value

FROM {{ ref('stg_order_items') }} AS oi

LEFT JOIN {{ ref('stg_orders') }} AS o
    ON oi.order_id = o.order_id
