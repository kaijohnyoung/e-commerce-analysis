from pathlib import Path
import pandas as pd
from utils import append_df_to_markdown, append_image_to_markdown
import matplotlib.pyplot as plt

# Read in raw datasets
datasets = {}

raw_data_folder = Path('./raw_data')

for file in raw_data_folder.iterdir():
    if file.is_file() and file.name != 'olist_geolocation_dataset.csv':
        datasets[file.name] = pd.read_csv(f'{raw_data_folder}/{file.name}')

# Get row counts for each dataset
row_counts = {}

for key, value in datasets.items():
    row_counts[key] = len(value)

append_df_to_markdown('outputs/exploratory_analysis.md', pd.DataFrame(row_counts.items(), columns=['Dataset','Row Count']), title = 'Row Counts by Dataset')

# Get column null counts for datasets with missing values 
for key, value in datasets.items():
    dataset_column_nulls = {}

    for col in value.columns:
        column_null_count = value[col].isna().sum()

        if column_null_count > 0:
            dataset_column_nulls[col] = int(column_null_count)

    if dataset_column_nulls:
        null_count_df = pd.DataFrame(dataset_column_nulls.items(), columns=['Column','Null Count'])

        null_count_df['Null Counts Expressed as a Percentage'] = (null_count_df['Null Count'] / len(value)) * 100
        
        append_df_to_markdown('outputs/exploratory_analysis.md', null_count_df, title = f'Columns with Missing Values in {key}')

# Create time series of orders by month
datasets['olist_orders_dataset.csv']['order_purchase_timestamp'] = pd.to_datetime(datasets['olist_orders_dataset.csv']['order_purchase_timestamp'])
datasets['olist_orders_dataset.csv']['Month'] = datasets['olist_orders_dataset.csv']['order_purchase_timestamp'].dt.to_period('M')

orders_by_month_df = pd.DataFrame(datasets['olist_orders_dataset.csv'].groupby('Month').size().reset_index(name='Order Counts'))

orders_by_month_df['Month'] = orders_by_month_df['Month'].astype(str)

plt.plot(orders_by_month_df['Month'], orders_by_month_df['Order Counts'])
plt.xticks(rotation=45)

plt.savefig('outputs/orders_time_series.png')

append_image_to_markdown('outputs/exploratory_analysis.md', 'orders_time_series.png',title = 'Time Series of Orders')

# Check foreign keys for main datasets
foreign_keys_to_check = (
    ['customer_id', 'olist_orders_dataset.csv','olist_customers_dataset.csv'],
    ['order_id', 'olist_order_items_dataset.csv','olist_orders_dataset.csv'],
    ['product_id', 'olist_order_items_dataset.csv', 'olist_products_dataset.csv'],
    ['seller_id', 'olist_order_items_dataset.csv', 'olist_sellers_dataset.csv'],
    ['order_id', 'olist_order_payments_dataset.csv', 'olist_orders_dataset.csv'],
    ['order_id', 'olist_order_reviews_dataset.csv', 'olist_orders_dataset.csv']
)

for check in foreign_keys_to_check:

    home_df = datasets[check[1]]
    df_to_check = datasets[check[2]]

    missing_keys_df = home_df[
        ~home_df[check[0]].isin(df_to_check[check[0]])
    ]

    append_df_to_markdown('outputs/exploratory_analysis.md', missing_keys_df[check[0]], title = f'{check[0]} in {check[1]} Not Present in {check[2]}')

# Count duplicate rows for each dataset
duplicate_checks = {}

for key, value in datasets.items():
    duplicate_checks[key] = int(value.duplicated().sum())

duplicate_checks_df = pd.DataFrame(duplicate_checks.items(), columns=['dataset', 'duplicate_count'])

append_df_to_markdown('outputs/exploratory_analysis.md', duplicate_checks_df, title = 'Count of Duplicate Rows in Each Dataset')

# Get distribution of sold item prices
sold_item_price_data = datasets['olist_order_items_dataset.csv']['price']

fig, ax = plt.subplots()

ax.hist(sold_item_price_data, bins='auto')
ax.set_ylabel('Count')
ax.set_xlabel('Sold Item Price')

fig.savefig('outputs/raw_sold_item_prices_histogram.png')

append_image_to_markdown('outputs/exploratory_analysis.md', 'raw_sold_item_prices_histogram.png', title = 'Histogram of Sold Item Prices')

# Get summary of prices
prices_summary = {
    'min': sold_item_price_data.min(),
    'max': sold_item_price_data.max(), 
    'median': sold_item_price_data.median(),
    'average': sold_item_price_data.mean() 
}

prices_summary_df = pd.DataFrame(prices_summary.items(),columns=['summary','value']).set_index('summary').T

append_df_to_markdown('outputs/exploratory_analysis.md', prices_summary_df, title='Summary of Sold Item Prices')

# Get distribution of sold item prices with new bins based on max price and log-transformed y-axis
from matplotlib.ticker import ScalarFormatter

fig1,ax1 = plt.subplots()

ax1.hist(sold_item_price_data,bins = int(prices_summary['max'] / 100) + 1)
ax1.set_yscale('log')
ax1.set_ylabel('Count (Log Scale)')
ax1.set_xlabel('Sold Item Price')
ax1.yaxis.set_major_formatter(ScalarFormatter())

fig1.savefig('outputs/adjusted_sold_item_prices_histogram.png')

append_image_to_markdown('outputs/exploratory_analysis.md', 'adjusted_sold_item_prices_histogram.png', title = 'Histogram of Sold Item Prices With Logged Y-Axis')