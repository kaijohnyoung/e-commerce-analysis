import pandas as pd
from pathlib import Path

# Query relevant columns for each dataset and store in datasets dictionary
datasets = {}

dataset_relevant_cols = {
    'olist_customers_dataset.csv' : ['customer_id', 'customer_unique_id', 'customer_city', 'customer_state'],
    'olist_orders_dataset.csv' : ['order_id', 'customer_id', 'order_status', 'order_purchase_timestamp'],
    'olist_order_items_dataset.csv' : ['order_id', 'order_item_id', 'product_id', 'seller_id', 'price', 'freight_value'],
    'olist_order_payments_dataset.csv' : ['order_id', 'payment_sequential', 'payment_type', 'payment_installments', 'payment_value'],
    'olist_order_reviews_dataset.csv' : ['review_id', 'order_id', 'review_score'],
    'olist_products_dataset.csv' : ['product_id', 'product_category_name'],
    'olist_sellers_dataset.csv' : ['seller_id', 'seller_city', 'seller_state'],
    'product_category_name_translation.csv' : ['product_category_name', 'product_category_name_english']
}

raw_data_folder = Path('./raw_data')

for file in raw_data_folder.iterdir():
    if file.is_file() and file.name != 'olist_geolocation_dataset.csv':
        datasets[file.name] = pd.read_csv(f'{raw_data_folder}/{file.name}')

        datasets[file.name] = datasets[file.name][dataset_relevant_cols[file.name]]

products = datasets['olist_products_dataset.csv']
customers = datasets['olist_customers_dataset.csv']
sellers = datasets['olist_sellers_dataset.csv']
order_items = datasets['olist_order_items_dataset.csv']
orders = datasets['olist_orders_dataset.csv']

# Translate product categories to English
products = products.merge(datasets['product_category_name_translation.csv'], how='left',on='product_category_name').drop(columns=['product_category_name'])
products = products.rename(columns={'product_category_name_english': 'product_category'})

# Assign NA values as 'Other' category
products['product_category'] = products['product_category'].fillna('Other')

# Standardise text columns of interest
products['product_category'] = products['product_category'].str.replace('_', ' ', regex=False).str.title()
customers['customer_city'] = customers['customer_city'].str.title()
sellers['seller_city'] = sellers['seller_city'].str.title()

# Get total units per order and total value per order
order_totals = (
    order_items
    .groupby('order_id', as_index=False)
    .agg(
        total_units_in_order=('order_item_id', 'count'),
        total_order_price=('price', 'sum')
    )
)

orders = orders.merge(order_totals, how='left', on='order_id')

# Categorise orders by dominant product category by value
item_categories = order_items.merge(products, how='left', on='product_id')

order_categories = (
    item_categories
    .groupby(['order_id', 'product_category'])['price'].sum().reset_index()
    .sort_values(by=['order_id', 'price'], ascending=False)
    .drop_duplicates('order_id')
    .rename(columns={'product_category': 'order_category'})
)

orders = orders.merge(order_categories[['order_id', 'order_category']], how='left', on='order_id')

datasets['olist_products_dataset.csv'] = products
datasets['olist_customers_dataset.csv'] = customers
datasets['olist_sellers_dataset.csv'] = sellers
datasets['olist_order_items_dataset.csv'] = order_items
datasets['olist_orders_dataset.csv'] = orders

# Load data into SQL database
from utils import get_engine
from sqlalchemy import text

engine = get_engine()

# Create tables in SQL database
sql_file_path = Path("scripts/create_tables.sql")
table_creation_sql = sql_file_path.read_text()

with engine.begin() as connection:
    connection.execute(text(table_creation_sql))

load_order = [
    'olist_customers_dataset.csv',
    'olist_orders_dataset.csv',
    'olist_products_dataset.csv',
    'olist_sellers_dataset.csv',
    'olist_order_items_dataset.csv',
    'olist_order_payments_dataset.csv',
    'olist_order_reviews_dataset.csv'
]

for file in load_order:

    df = datasets[file]
    table_name = file.removeprefix('olist_').removesuffix('_dataset.csv')
    df.to_sql(table_name, engine, index=False, if_exists='append')