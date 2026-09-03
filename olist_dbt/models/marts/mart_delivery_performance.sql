SELECT
    order_id,
    customer_id,
    order_date,
    order_status,

    order_purchase_timestamp,
    order_approved_at,
    order_delivered_carrier_date,
    order_delivered_customer_date,
    order_estimated_delivery_date,

    DATE_DIFF(
        DATE(order_delivered_customer_date),
        DATE(order_purchase_timestamp),
        DAY
    ) AS delivery_days,

    DATE_DIFF(
        DATE(order_delivered_customer_date),
        DATE(order_estimated_delivery_date),
        DAY
    ) AS delivery_delay_days,

    CASE
        WHEN order_delivered_customer_date IS NULL THEN 'Not Delivered'
        WHEN DATE(order_delivered_customer_date)
             <= DATE(order_estimated_delivery_date)
            THEN 'On Time'
        ELSE 'Late'
    END AS delivery_performance

FROM {{ ref('fact_orders') }}
