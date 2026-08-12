import numpy as np
import pandas as pd

import joblib
from sklearn.preprocessing import MinMaxScaler, StandardScaler, OneHotEncoder
from category_encoders.count import CountEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.compose import ColumnTransformer

from sklearn.metrics.pairwise import cosine_similarity

from data_cleaning import data_for_content_filtering

from scipy.sparse import save_npz

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
cleaned_data_path = PROJECT_ROOT / "data" / "cleaned_data.csv"




frequency_cols = ['year']
ohe_cols = ['artist','time_signature','key']
tfidf_col = 'tags'
standard_scale_cols = ['duration_ms','loudness','tempo']
min_max_scaler = ['danceability','energy','speechiness','acousticness','instrumentalness','liveness','valence']


def train_transformer(data):


    transformer = ColumnTransformer(
    transformers=[
        ("frequency_encoder", CountEncoder(normalize=True, return_df=True), frequency_cols),
        ("ohe", OneHotEncoder(handle_unknown="ignore"), ohe_cols),
        ("tfidf", TfidfVectorizer(max_features=85), tfidf_col),
        ("standard_scaler", StandardScaler(), standard_scale_cols),
        ("MinMaxScaler", MinMaxScaler(), min_max_scaler)
    ],
    remainder="passthrough",
    n_jobs=-1,
    )

    transformer.fit(data)
    joblib.dump(transformer,'transformer.joblib')


def transform_data(data):

    transformer = joblib.load('transformer.joblib')

    transformed_data = transformer.transform(data)

    return transformed_data


def save_transformed_data(transformed_data,data_path):

    save_npz(data_path, transformed_data)



def calculate_similarity_score(input_vector , data):

    similarity_score = cosine_similarity(input_vector , data)

    return similarity_score




def recommend(song_name,songs_data,transformed_data,k):

    song_row = songs_data.loc[songs_data['name'] == song_name.lower(),:]
    
    if song_row.empty:
        print("song not found in the dataset")

    else:
        song_name = song_name.lower().strip()
        song_row = songs_data.loc[songs_data['name'] == song_name]
        song_index = song_row.index[0]

        input_vector = transformed_data[song_index].reshape(1,-1)
        similarity_scores = calculate_similarity_score(input_vector,transformed_data)
        top_k_songs_indexes = np.argsort(similarity_scores.ravel())[-k-1:][::-1]

        top_k_songs_names = songs_data.iloc[top_k_songs_indexes]
        top_k_list = top_k_songs_names[['name','artist','spotify_preview_url']].reset_index(drop = True)
        return top_k_list


def test_recommendations(data_path,song_name,k=10):

    song_name = song_name.lower().strip()
    data = pd.read_csv(data_path)

    data_content_filtering = data_for_content_filtering(data)

    train_transformer(data_content_filtering)

    transformed_data = transform_data(data_content_filtering)

    save_transformed_data(transformed_data,"data/transformed_data.npz")


    song_row = data.loc[data['name'] == song_name]
    print(song_row)

    song_index = song_row.index[0]

    input_vector = transformed_data[song_index].reshape(1,-1)
    similarity_scores = calculate_similarity_score(input_vector,transformed_data)
    top_k_songs_indexes = np.argsort(similarity_scores.ravel())[-k-1:][::-1]

    top_k_songs_names = data.iloc[top_k_songs_indexes]
    top_k_list = top_k_songs_names[['name','artist','spotify_preview_url']].reset_index(drop = True)
    print(top_k_list)

if __name__ == '__main__':

    test_recommendations(cleaned_data_path,"Hips Don't Lie",10)