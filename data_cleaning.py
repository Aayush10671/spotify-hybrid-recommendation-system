import pandas as pd

data_path = "../data/Music_Info"

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

     return (data.drop(columns = ['track_id','name','spotify_preview']))


def main(data_path):
     data = pd.read_csv(data_path)

     cleaned_data = clean_data(data_path)

     cleaned_data.to_csv("data/cleaned_data.csv",index = False)


if __name__ == "__main__":
     main(data_path)