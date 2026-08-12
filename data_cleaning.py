import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
data_path = PROJECT_ROOT / "data" / "Music_Info.csv"
output_path = PROJECT_ROOT / "data" / "cleaned_data.csv"

def clean_data(data):

    data.drop_duplicates(subset=['spotify_id'], inplace=True)
    data.drop(columns=['genre', 'spotify_id'], inplace=True)
    data.fillna({'tags': 'no_tags'}, inplace=True)
    data['name'] = data['name'].str.lower().str.strip()
    data['artist'] = data['artist'].str.lower().str.strip()
    data['tags'] = data['tags'].str.lower()
    data.reset_index(drop=True, inplace=True)

    return data


def data_for_content_filtering(data):
    columns_to_drop = ['track_id', 'name', 'spotify_preview_url']

    return data.drop(
        columns=columns_to_drop,
        errors='ignore'
    )

def main(data_path):
     data = pd.read_csv(data_path)

     cleaned_data = clean_data(data)

     cleaned_data.to_csv(output_path,index = False)


if __name__ == "__main__":
     main(data_path)