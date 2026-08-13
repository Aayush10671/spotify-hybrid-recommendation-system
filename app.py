import streamlit as st
from content_based_filtering import recommend
from scipy.sparse import load_npz
import pandas as pd
from pathlib import Path
from collaborative_filtering import collaborative_recommendation
from numpy import load

PROJECT_ROOT = Path(__file__).resolve().parent

transformed_data_path = PROJECT_ROOT / "data" / "transformed_data.npz"
cleaned_data = PROJECT_ROOT / "data" / "cleaned_data.csv"
track_ids_path = PROJECT_ROOT / 'data' / 'track_ids.npy'
track_ids = load(track_ids_path,allow_pickle = True)

filtered_data_path =  PROJECT_ROOT / 'data' / 'collab_filtered_data.csv' 
filtered_data = pd.read_csv(filtered_data_path)

interaction_matrix_path =  PROJECT_ROOT / 'data' / 'interaction_matrix.npz'
interaction_matrix = load_npz(interaction_matrix_path)


data = pd.read_csv(cleaned_data)
transformed_data = load_npz(transformed_data_path)

st.title("Welcome To The Spotify Songs Recommender")

song_name = st.text_input("Enter a song name: ")
st.write("You entered:", song_name)

artist_name = st.text_input("Enter the artist name---")

artist_name = artist_name.lower().strip()  
song_name = song_name.lower().strip()

k = st.selectbox("How Many Recommendations Do You Want??", [5, 10, 15, 20], index=1)
filtering_type = st.selectbox("Select the type of filtering",['content-based filtering','collaborative filtering'])


if filtering_type == 'content-based filtering':
    if st.button('Get Recommendation'):
        if ((data['artist'] ==artist_name ) & (data['name'].str.lower() == song_name)).any():
            st.write('Recommendation for', f"**{song_name}**")
            
            recommendations = recommend(song_name, artist_name,data, transformed_data, k)
            
            if not recommendations.empty:
                for ind, recommendation in recommendations.iterrows():
                    song_name_title = recommendation['name'].title()
                    artist_name = recommendation['artist'].title()
                    
                    if ind == 0:
                        st.markdown("## Current song ##")
                        st.markdown(f"##** **{song_name_title}** by **{artist_name}** **##")
                        if pd.notna(recommendation['spotify_preview_url']):
                            st.audio(recommendation['spotify_preview_url'])
                        st.write("-----")
                    elif ind == 1:
                        st.markdown("Next song")
                        st.markdown(f"##** {ind}.**{song_name_title}** by **{artist_name}****##")
                        if pd.notna(recommendation['spotify_preview_url']):
                            st.audio(recommendation['spotify_preview_url'])
                        st.write("-----")
                    else:
                        st.markdown(f"##** {ind}.**{song_name_title}** by **{artist_name}****##")
                        if pd.notna(recommendation['spotify_preview_url']):
                            st.audio(recommendation['spotify_preview_url'])
                        st.write("-----")
            else:
                st.write("No recommendations found for this song.")
        else:
            st.write(f"Sorry, we couldn't find '{song_name}' in the dataset. Please try another song")


elif filtering_type == 'collaborative filtering':

   if st.button('Get Recommendation'):
           if ((filtered_data['artist'].str.lower() == artist_name) & (filtered_data['name'].str.lower() == song_name)).any():
               st.write('Recommendation for', f"**{song_name}**")

               try:
                   recommendations = collaborative_recommendation(song_name,artist_name,track_ids,filtered_data,interaction_matrix,k)
               except ValueError as e:
                   st.write(str(e))
                   recommendations = pd.DataFrame()

               if not recommendations.empty:
                   for ind, recommendation in recommendations.iterrows():
                       song_name_title = recommendation['name'].title()
                       artist_name = recommendation['artist'].title()
                       
                       if ind == 0:
                           st.markdown("## Current song ##")
                           st.markdown(f"##** **{song_name_title}** by **{artist_name}** **##")
                           if pd.notna(recommendation['spotify_preview_url']):
                               st.audio(recommendation['spotify_preview_url'])
                           st.write("-----")
                       elif ind == 1:
                           st.markdown("Next song")
                           st.markdown(f"##** {ind}.**{song_name_title}** by **{artist_name}****##")
                           if pd.notna(recommendation['spotify_preview_url']):
                               st.audio(recommendation['spotify_preview_url'])
                           st.write("-----")
                       else:
                           st.markdown(f"##** {ind}.**{song_name_title}** by **{artist_name}****##")
                           if pd.notna(recommendation['spotify_preview_url']):
                               st.audio(recommendation['spotify_preview_url'])
                           st.write("-----")
               else:
                   st.write("No recommendations found for this song.")
           else:
               st.write(f"Sorry, we couldn't find '{song_name}' in the dataset. Please try another song")