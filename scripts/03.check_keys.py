from pathlib import Path
import pandas as pd
from utils import append_df_to_markdown

# Read in raw datasets
datasets = {}

raw_data_folder = Path('./raw_data')

for file in raw_data_folder.iterdir():
    if file.is_file() and file.name != 'olist_geolocation_dataset.csv':
        datasets[file.name] = pd.read_csv(f'{raw_data_folder}/{file.name}')

# Identify candidates for primary keys in each dataset
primary_key_candidates = {}

for dataset_name, dataset in datasets.items():

    primary_key_candidates[dataset_name] = []

    for col in dataset.columns:
        unique_check = dataset[col].nunique() == len(dataset)

        if unique_check:
            primary_key_candidates[dataset_name].append(col)

pk_rows = []

for dataset_name,primary_keys in primary_key_candidates.items():
    row = {
        "dataset": dataset_name,
        "primary_key_candidates": primary_keys
    }

    pk_rows.append(row)

primary_key_candidates_df = pd.DataFrame(pk_rows)

append_df_to_markdown('./outputs/key_investigation_results.md', primary_key_candidates_df, title="1. Possible Primary Keys for Raw Datasets")

# Returns a bool to determine if a pairs of columns is a candidate to be a compound key
def check_compound_key(data, col1, col2):

    not_null_check1 = data[col1].isna().sum() == 0
    not_null_check2 = data[col2].isna().sum() == 0

    data['compound_key'] = data[col1].astype(str) + '_' + data[col2].astype(str) 

    uniqueness_check = data['compound_key'].nunique() == len(data)

    data.drop(columns='compound_key', inplace=True)

    return not_null_check1 and not_null_check2 and uniqueness_check

# Identify candidates for compound keys in each dataset
compound_key_candidates = {}

for dataset_name, dataset in datasets.items():

    if dataset_name == 'olist_order_items_dataset.csv' and check_compound_key(dataset, 'order_id', 'order_item_id'):
        compound_key_candidates[dataset_name] = ['order_id', 'order_item_id']

    elif dataset_name == 'olist_order_payments_dataset.csv' and check_compound_key(dataset, 'order_id', 'payment_sequential'):
        compound_key_candidates[dataset_name] = ['order_id', 'payment_sequential']

    elif dataset_name == 'olist_order_reviews_dataset.csv' and check_compound_key(dataset, 'review_id', 'order_id'):
        compound_key_candidates[dataset_name] = ['review_id', 'order_id']
    
ck_rows = []

for dataset_name, compound_keys in compound_key_candidates.items():
    row = {
        "dataset": dataset_name,
        "compound_key_candidates": compound_keys
    }

    ck_rows.append(row)

compound_key_candidates_df = pd.DataFrame(ck_rows)

append_df_to_markdown('./outputs/key_investigation_results.md', compound_key_candidates_df, title="2. Compound Keys for Raw Datasets")

# Check foreign keys for main datasets
foreign_keys_to_check = (
    ['customer_id', 'olist_orders_dataset.csv','olist_customers_dataset.csv'],
    ['order_id', 'olist_order_items_dataset.csv','olist_orders_dataset.csv'],
    ['product_id', 'olist_order_items_dataset.csv', 'olist_products_dataset.csv'],
    ['seller_id', 'olist_order_items_dataset.csv', 'olist_sellers_dataset.csv'],
    ['order_id', 'olist_order_payments_dataset.csv', 'olist_orders_dataset.csv'],
    ['order_id', 'olist_order_reviews_dataset.csv', 'olist_orders_dataset.csv']
)

missing_key_results = []

for key, child_name, parent_name in foreign_keys_to_check:

    child_df = datasets[child_name]
    parent_df = datasets[parent_name]

    missing_count = int((~child_df[key].isin(parent_df[key])).sum())

    if missing_count == 0:
        description = f"There is at least one matching {key} in {parent_name} for each {key} in {child_name}"
    elif missing_count == 1:
        description = f"{missing_count} value of {key} in {child_name} has no match in {parent_name}"
    else:
        description = f"{missing_count} values of {key} in {child_name} have no match in {parent_name}"

    missing_key_results.append(
        {
            'Key': key,
            'Child Dataset': child_name,
            'Parent Dataset': parent_name,
            'Rows Without Match': missing_count,
            'Description': description
        }
    )

    missing_count_reverse = int((~parent_df[key].isin(child_df[key])).sum())

    if missing_count_reverse == 0:
        description = f"There is at least one matching {key} in {child_name} for each {key} in {parent_name}"
    elif missing_count_reverse == 1:
        description = f"{missing_count_reverse} value of {key} in {parent_name} has no match in {child_name}"
    else:
        description = f"{missing_count_reverse} values of {key} in {parent_name} have no match in {child_name}"

    missing_key_results.append(
            {
                'Key': key,
                'Child Dataset': parent_name,
                'Parent Dataset': child_name,
                'Rows Without Match': missing_count_reverse,
                'Description': description
            }
        )

append_df_to_markdown('outputs/key_investigation_results.md', pd.DataFrame(missing_key_results), title = '3. Foreign Key Check Results')