SELECT
    string_field_0 AS product_category_name,
    string_field_1 AS product_category_name_english
FROM {{ source('raw_sales', 'product_category_name_translation') }}
