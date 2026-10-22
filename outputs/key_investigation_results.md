## 1. Possible Primary Keys for Raw Datasets

| dataset                               | primary_key_candidates                                     |
|:--------------------------------------|:-----------------------------------------------------------|
| olist_customers_dataset.csv           | ['customer_id']                                            |
| olist_orders_dataset.csv              | ['order_id', 'customer_id']                                |
| olist_order_items_dataset.csv         | []                                                         |
| olist_order_payments_dataset.csv      | []                                                         |
| olist_order_reviews_dataset.csv       | []                                                         |
| olist_products_dataset.csv            | ['product_id']                                             |
| olist_sellers_dataset.csv             | ['seller_id']                                              |
| product_category_name_translation.csv | ['product_category_name', 'product_category_name_english'] |

## 2. Compound Keys for Raw Datasets

| dataset                          | compound_key_candidates            |
|:---------------------------------|:-----------------------------------|
| olist_order_items_dataset.csv    | ['order_id', 'order_item_id']      |
| olist_order_payments_dataset.csv | ['order_id', 'payment_sequential'] |
| olist_order_reviews_dataset.csv  | ['review_id', 'order_id']          |

## 3. Foreign Key Check Results

| Key         | Child Dataset                    | Parent Dataset                   |   Rows Without Match | Description                                                                                                                  |
|:------------|:---------------------------------|:---------------------------------|---------------------:|:-----------------------------------------------------------------------------------------------------------------------------|
| customer_id | olist_orders_dataset.csv         | olist_customers_dataset.csv      |                    0 | There is at least one matching customer_id in olist_customers_dataset.csv for each customer_id in olist_orders_dataset.csv   |
| customer_id | olist_customers_dataset.csv      | olist_orders_dataset.csv         |                    0 | There is at least one matching customer_id in olist_orders_dataset.csv for each customer_id in olist_customers_dataset.csv   |
| order_id    | olist_order_items_dataset.csv    | olist_orders_dataset.csv         |                    0 | There is at least one matching order_id in olist_orders_dataset.csv for each order_id in olist_order_items_dataset.csv       |
| order_id    | olist_orders_dataset.csv         | olist_order_items_dataset.csv    |                  775 | 775 values of order_id in olist_orders_dataset.csv have no match in olist_order_items_dataset.csv                            |
| product_id  | olist_order_items_dataset.csv    | olist_products_dataset.csv       |                    0 | There is at least one matching product_id in olist_products_dataset.csv for each product_id in olist_order_items_dataset.csv |
| product_id  | olist_products_dataset.csv       | olist_order_items_dataset.csv    |                    0 | There is at least one matching product_id in olist_order_items_dataset.csv for each product_id in olist_products_dataset.csv |
| seller_id   | olist_order_items_dataset.csv    | olist_sellers_dataset.csv        |                    0 | There is at least one matching seller_id in olist_sellers_dataset.csv for each seller_id in olist_order_items_dataset.csv    |
| seller_id   | olist_sellers_dataset.csv        | olist_order_items_dataset.csv    |                    0 | There is at least one matching seller_id in olist_order_items_dataset.csv for each seller_id in olist_sellers_dataset.csv    |
| order_id    | olist_order_payments_dataset.csv | olist_orders_dataset.csv         |                    0 | There is at least one matching order_id in olist_orders_dataset.csv for each order_id in olist_order_payments_dataset.csv    |
| order_id    | olist_orders_dataset.csv         | olist_order_payments_dataset.csv |                    1 | 1 value of order_id in olist_orders_dataset.csv has no match in olist_order_payments_dataset.csv                             |
| order_id    | olist_order_reviews_dataset.csv  | olist_orders_dataset.csv         |                    0 | There is at least one matching order_id in olist_orders_dataset.csv for each order_id in olist_order_reviews_dataset.csv     |
| order_id    | olist_orders_dataset.csv         | olist_order_reviews_dataset.csv  |                  768 | 768 values of order_id in olist_orders_dataset.csv have no match in olist_order_reviews_dataset.csv                          |

