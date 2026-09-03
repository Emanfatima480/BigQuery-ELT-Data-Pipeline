SELECT
    o.order_id,
    o.customer_id,
    DATE(o.order_purchase_timestamp) AS order_date,
    o.order_status,

    o.order_purchase_timestamp,
    o.order_approved_at,
    o.order_delivered_carrier_date,
    o.order_delivered_customer_date,
    o.order_estimated_delivery_date

FROM {{ ref('stg_orders') }} AS o
