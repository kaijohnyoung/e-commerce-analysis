from pathlib import Path
import kagglehub
import pandas as pd
from utils import append_df_to_markdown

# Use Kaggle API to download data
raw_data_folder = Path('./raw_data')

kagglehub.dataset_download(
    'olistbr/brazilian-ecommerce',
    output_dir=raw_data_folder,
    force_download=True
)

for file in raw_data_folder.iterdir():
    if file.is_file() and file.name != 'olist_geolocation_dataset.csv':
        temp_df = pd.read_csv(file)

        append_df_to_markdown('./outputs/raw_data_previews.md', temp_df.head(10), title=f"'{file.name}' Dataset Preview")