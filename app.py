# import streamlit as st
# from content_based_filtering import recommend
# from scipy.sparse import load_npz
# import pandas as pd
# from pathlib import Path
# from collaborative_filtering import collaborative_recommendation
# from numpy import load
# from hybrid_recommendation import HybridRecommenderSystem as hrs

# PROJECT_ROOT = Path(__file__).resolve().parent

# transformed_data_path = PROJECT_ROOT / "data" / "transformed_data.npz"
# cleaned_data = PROJECT_ROOT / "data" / "cleaned_data.csv"
# track_ids_path = PROJECT_ROOT / 'data' / 'track_ids.npy'

# transform_hybrid_path = PROJECT_ROOT / 'data' / 'transformed_hybrid_data.npz'
# st.session_state.transformed_hybrid_data = load_npz(transform_hybrid_path)


# st.session_state.track_ids = load(track_ids_path,allow_pickle = True)

# filtered_data_path =  PROJECT_ROOT / 'data' / 'collab_filtered_data.csv' 
# st.session_state.filtered_data = pd.read_csv(filtered_data_path)

# interaction_matrix_path =  PROJECT_ROOT / 'data' / 'interaction_matrix.npz'
# st.session_state.interaction_matrix = load_npz(interaction_matrix_path)
# st.session_state.interaction_matrix = (
#     st.session_state.interaction_matrix[
#         :len(st.session_state.filtered_data)
#     ]
# )

# st.session_state.data = pd.read_csv(cleaned_data)
# st.session_state.transformed_data = load_npz(transformed_data_path)

# st.session_state.track_ids = (
#     st.session_state.track_ids[
#         :len(st.session_state.filtered_data)
#     ]
# )

# st.title("Welcome To The Spotify Songs Recommender")

# song_name = st.text_input("Enter a song name: ")
# st.write("You entered:", song_name)

# artist_name = st.text_input("Enter the artist name---")

# artist_name = artist_name.lower().strip()  
# song_name = song_name.lower().strip()

# k = st.selectbox("How Many Recommendations Do You Want??", [5, 10, 15, 20], index=1)

# if((st.session_state.filtered_data['name'].str.lower() == song_name) & (st.session_state.filtered_data['artist'].str.lower() == artist_name)).any():
#     filtering_type = st.selectbox("Select the type of filtering",['content-based filtering','collaborative filtering','Hybrid Recommender System'],index=2)

#     diversity = st.slider(label = "diversity of recommendation",min_value = 1 , max_value = 10 , value = 5,step = 1)

#     content_based_weight = 1- (diversity/10)

# else:
#     filtering_type = st.selectbox("Select the type of filtering",['content-based filtering'])


# if filtering_type == 'content-based filtering':
#     if st.button('Get Recommendation'):
#         if ((st.session_state.data['artist'].str.lower() ==artist_name ) & (st.session_state.data['name'].str.lower() == song_name)).any():
#             st.write('Recommendation for', f"**{song_name}**")
            
#             recommendations = recommend(song_name, artist_name,st.session_state.data, st.session_state.transformed_data, k)
            
#             if not recommendations.empty:
#                 for ind, recommendation in recommendations.iterrows():
#                     song_name_title = recommendation['name'].title()
#                     artist_name = recommendation['artist'].title()
                    
#                     if ind == 0:
#                         st.markdown("## Current song ##")
#                         st.markdown(f"##** **{song_name_title}** by **{artist_name}** **##")
#                         if pd.notna(recommendation['spotify_preview_url']):
#                             st.audio(recommendation['spotify_preview_url'])
#                         st.write("-----")
#                     elif ind == 1:
#                         st.markdown("Next song")
#                         st.markdown(f"##** {ind}.**{song_name_title}** by **{artist_name}****##")
#                         if pd.notna(recommendation['spotify_preview_url']):
#                             st.audio(recommendation['spotify_preview_url'])
#                         st.write("-----")
#                     else:
#                         st.markdown(f"##** {ind}.**{song_name_title}** by **{artist_name}****##")
#                         if pd.notna(recommendation['spotify_preview_url']):
#                             st.audio(recommendation['spotify_preview_url'])
#                         st.write("-----")
#             else:
#                 st.write("No recommendations found for this song.")
#         else:
#             st.write(f"Sorry, we couldn't find '{song_name}' in the dataset. Please try another song")


# elif filtering_type == 'collaborative filtering':
#    if st.button('Get Recommendation'):
#            if ((st.session_state.filtered_data['artist'].str.lower() == artist_name) & (st.session_state.filtered_data['name'].str.lower() == song_name)).any():
#                st.write('Recommendation for', f"**{song_name}**")

#                try:
#                    recommendations = collaborative_recommendation(song_name,artist_name,st.session_state.track_ids,st.session_state.filtered_data,st.session_state.interaction_matrix,k)
#                except ValueError as e:
#                    st.write(str(e))
#                    recommendations = pd.DataFrame()

#                if not recommendations.empty:
#                    for ind, recommendation in recommendations.iterrows():
#                        song_name_title = recommendation['name'].title()
#                        artist_name = recommendation['artist'].title()
                       
#                        if ind == 0:
#                            st.markdown("## Current song ##")
#                            st.markdown(f"##** **{song_name_title}** by **{artist_name}** **##")
#                            if pd.notna(recommendation['spotify_preview_url']):
#                                st.audio(recommendation['spotify_preview_url'])
#                            st.write("-----")
#                        elif ind == 1:
#                            st.markdown("Next song")
#                            st.markdown(f"##** {ind}.**{song_name_title}** by **{artist_name}****##")
#                            if pd.notna(recommendation['spotify_preview_url']):
#                                st.audio(recommendation['spotify_preview_url'])
#                            st.write("-----")
#                        else:
#                            st.markdown(f"##** {ind}.**{song_name_title}** by **{artist_name}****##")
#                            if pd.notna(recommendation['spotify_preview_url']):
#                                st.audio(recommendation['spotify_preview_url'])
#                            st.write("-----")
#                else:
#                    st.write("No recommendations found for this song.")
#            else:
#                st.write(f"Sorry, we couldn't find '{song_name}' in the dataset. Please try another song")

# if filtering_type == 'Hybrid Recommender System':


#      if st.button('Get Recommendation'):
#                if ((st.session_state.filtered_data['artist'].str.lower() == artist_name) & (st.session_state.filtered_data['name'].str.lower() == song_name)).any():
#                    st.write('Recommendation for', f"**{song_name}**")
    
#                    try:
#                        recommender = hrs(k,content_based_weight)
#                        recommendations = recommender.give_recommendations(song_name,artist_name,st.session_state.filtered_data,st.session_state.track_ids,st.session_state.transformed_hybrid_data,st.session_state.interaction_matrix)
#                    except ValueError as e:
#                        st.write("filtered_data shape:", st.session_state.filtered_data.shape)
#                        st.write("track_ids shape:", st.session_state.track_ids.shape)
#                        st.write("hybrid matrix shape:", st.session_state.transformed_hybrid_data.shape)
#                        st.write("interaction matrix shape:", st.session_state.interaction_matrix.shape)
#                        st.write("hybrid recommendation system failed")
#                        st.write(e)
#                        recommendations = pd.DataFrame()
    
#                    if not recommendations.empty:
#                        for ind, recommendation in recommendations.iterrows():
#                            song_name_title = recommendation['name'].title()
#                            artist_name = recommendation['artist'].title()
                           
#                            if ind == 0:
#                                st.markdown("## Current song ##")
#                                st.markdown(f"##** **{song_name_title}** by **{artist_name}** **##")
#                                if pd.notna(recommendation['spotify_preview_url']):
#                                    st.audio(recommendation['spotify_preview_url'])
#                                st.write("-----")
#                            elif ind == 1:
#                                st.markdown("Next song")
#                                st.markdown(f"##** {ind}.**{song_name_title}** by **{artist_name}****##")
#                                if pd.notna(recommendation['spotify_preview_url']):
#                                    st.audio(recommendation['spotify_preview_url'])
#                                st.write("-----")
#                            else:
#                                st.markdown(f"##** {ind}.**{song_name_title}** by **{artist_name}****##")
#                                if pd.notna(recommendation['spotify_preview_url']):
#                                    st.audio(recommendation['spotify_preview_url'])
#                                st.write("-----")
#                    else:
#                        st.write("No recommendations found for this song.")
#                else:
#                    st.write(f"Sorry, we couldn't find '{song_name}' in the dataset. Please try another song")


####...............................added some design to ui using ai........................................................


import streamlit as st
from content_based_filtering import recommend
from scipy.sparse import load_npz
import pandas as pd
from pathlib import Path
from collaborative_filtering import collaborative_recommendation
from numpy import load
from hybrid_recommendation import HybridRecommenderSystem as hrs


# ---------------------------------------------------------------------------
# Page config — must be the first Streamlit command
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Spotify Songs Recommender",
    page_icon="🎧",
    layout="centered",
)

# ---------------------------------------------------------------------------
# DESIGN ONLY — global CSS injection (Spotify-inspired dark theme)
# No app logic lives below this block.
# ---------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800&family=Poppins:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: radial-gradient(circle at top left, #1a1a1a 0%, #121212 45%, #000000 100%);
    color: #FFFFFF;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
[data-testid="stHeader"] {background: transparent;}

.block-container {
    padding-top: 2.2rem;
    max-width: 780px;
}

/* ---------- Hero ---------- */
.hero-wrap {
    text-align: center;
    padding: 0.5rem 0 2rem 0;
}
.hero-eyebrow {
    color: #1DB954;
    font-weight: 600;
    letter-spacing: 3px;
    font-size: 0.75rem;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.hero-title {
    font-family: 'Montserrat', sans-serif;
    font-weight: 800;
    font-size: 2.5rem;
    color: #FFFFFF;
    margin: 0;
    line-height: 1.15;
}
.hero-title span { color: #1DB954; }
.hero-sub {
    color: #B3B3B3;
    font-size: 0.95rem;
    margin-top: 0.6rem;
}

/* ---------- Search card ---------- */
.search-card {
    background: #181818;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    padding: 1.3rem 1.4rem 0.3rem 1.4rem;
    margin-bottom: 1.4rem;
}
.section-label {
    color: #B3B3B3;
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    margin: 0.2rem 0 0.6rem 0;
}

/* ---------- Inputs ---------- */
[data-testid="stTextInput"] input {
    background-color: #2a2a2a !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 24px !important;
    padding: 0.55rem 1rem !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: #1DB954 !important;
    box-shadow: 0 0 0 1px #1DB954 !important;
}
[data-testid="stTextInput"] label,
[data-testid="stSelectbox"] label,
[data-testid="stSlider"] label {
    color: #B3B3B3 !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* ---------- Selectbox ---------- */
[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background-color: #2a2a2a !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
    color: #FFFFFF !important;
}

/* ---------- Slider ---------- */
[data-testid="stSlider"] [role="slider"] {
    background-color: #1DB954 !important;
    border-color: #1DB954 !important;
}

/* ---------- Buttons ---------- */
[data-testid="stButton"] button {
    background-color: #1DB954 !important;
    color: #000000 !important;
    border: none !important;
    border-radius: 500px !important;
    padding: 0.6rem 2.4rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    font-size: 0.8rem !important;
    transition: all 0.15s ease-in-out;
}
[data-testid="stButton"] button:hover {
    background-color: #1ED760 !important;
    transform: scale(1.03);
    color: #000000 !important;
}

/* ---------- Track cards ---------- */
.track-card {
    background: #181818;
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 12px;
    padding: 0.9rem 1.2rem;
    margin-bottom: 0.5rem;
    transition: background 0.15s ease-in-out;
}
.track-card:hover {
    background: #232323;
}
.current-track {
    border-left: 4px solid #1DB954;
    background: #16241c;
}
.track-title {
    font-family: 'Montserrat', sans-serif;
    font-weight: 700;
    font-size: 1.05rem;
    color: #FFFFFF;
    margin-top: 0.25rem;
}
.track-artist {
    color: #B3B3B3;
    font-size: 0.85rem;
}
.track-number {
    display: inline-block;
    width: 24px;
    height: 24px;
    line-height: 24px;
    text-align: center;
    background: rgba(255,255,255,0.08);
    color: #B3B3B3;
    border-radius: 50%;
    font-size: 0.72rem;
    font-weight: 600;
    margin-bottom: 0.35rem;
}
.track-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 1px;
    padding: 3px 10px;
    border-radius: 500px;
    margin-bottom: 0.4rem;
}
.now-playing-badge {
    background: rgba(29,185,84,0.15);
    color: #1DB954;
}
.up-next-badge {
    background: rgba(255,255,255,0.08);
    color: #B3B3B3;
}

/* Equalizer animation for the "now playing" card */
.eq-bar {
    display: inline-block;
    width: 3px;
    height: 8px;
    background: #1DB954;
    animation: eq 0.9s ease-in-out infinite;
    border-radius: 1px;
}
.eq-bar:nth-child(2) { animation-delay: 0.2s; }
.eq-bar:nth-child(3) { animation-delay: 0.4s; }
@keyframes eq {
    0%, 100% { height: 4px; }
    50% { height: 12px; }
}

/* ---------- Audio player, dark tint ---------- */
[data-testid="stAudio"] audio {
    width: 100%;
    filter: invert(90%) hue-rotate(180deg) brightness(0.95);
    border-radius: 8px;
}

/* ---------- Alerts ---------- */
[data-testid="stAlert"] {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)


PROJECT_ROOT = Path(__file__).resolve().parent

transformed_data_path = PROJECT_ROOT / "data" / "transformed_data.npz"
cleaned_data = PROJECT_ROOT / "data" / "cleaned_data.csv"
track_ids_path = PROJECT_ROOT / 'data' / 'track_ids.npy'

transform_hybrid_path = PROJECT_ROOT / 'data' / 'transformed_hybrid_data.npz'
st.session_state.transformed_hybrid_data = load_npz(transform_hybrid_path)


st.session_state.track_ids = load(track_ids_path, allow_pickle=True)

filtered_data_path = PROJECT_ROOT / 'data' / 'collab_filtered_data.csv'
st.session_state.filtered_data = pd.read_csv(filtered_data_path)

interaction_matrix_path = PROJECT_ROOT / 'data' / 'interaction_matrix.npz'
st.session_state.interaction_matrix = load_npz(interaction_matrix_path)
st.session_state.interaction_matrix = (
    st.session_state.interaction_matrix[
        :len(st.session_state.filtered_data)
    ]
)


st.session_state.data = pd.read_csv(cleaned_data)
st.session_state.transformed_data = load_npz(transformed_data_path)

st.session_state.track_ids = (
    st.session_state.track_ids[
        :len(st.session_state.filtered_data)
    ]
)

# ---------------------------------------------------------------------------
# DESIGN ONLY — hero header (replaces st.title, same page purpose)
# ---------------------------------------------------------------------------
st.markdown("""
<div class="hero-wrap">
    <div class="hero-eyebrow">🎧 Discover something new</div>
    <div class="hero-title">Spotify <span>Songs</span> Recommender</div>
    <div class="hero-sub">Tell us a track you love, and we'll line up what to play next.</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="search-card">', unsafe_allow_html=True)
st.markdown('<div class="section-label">🔍 Find a song</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    song_name = st.text_input("Enter a song name: ")
with col2:
    artist_name = st.text_input("Enter the artist name---")

st.write("You entered:", song_name)

artist_name = artist_name.lower().strip()
song_name = song_name.lower().strip()

k = st.selectbox("How Many Recommendations Do You Want??", [5, 10, 15, 20], index=1)

if ((st.session_state.filtered_data['name'].str.lower() == song_name) & (st.session_state.filtered_data['artist'].str.lower() == artist_name)).any():
    filtering_type = st.selectbox("Select the type of filtering", ['content-based filtering', 'collaborative filtering', 'Hybrid Recommender System'], index=2)

    diversity = st.slider(label="diversity of recommendation", min_value=1, max_value=10, value=5, step=1)

    content_based_weight = 1 - (diversity / 10)

else:
    filtering_type = st.selectbox("Select the type of filtering", ['content-based filtering'])

st.markdown('</div>', unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# DESIGN ONLY — shared card renderer.
# All three branches below rendered this exact block inline before; the
# markup is identical for all of them, so it's pulled out here purely to
# keep the styling in one place. No behavior changes.
# ---------------------------------------------------------------------------
def render_song_card(recommendation, ind):
    song_name_title = recommendation['name'].title()
    artist_name_title = recommendation['artist'].title()

    if ind == 0:
        st.markdown(f"""
        <div class="track-card current-track">
            <div class="track-badge now-playing-badge">
                <span class="eq-bar"></span><span class="eq-bar"></span><span class="eq-bar"></span>
                NOW PLAYING
            </div>
            <div class="track-title">{song_name_title}</div>
            <div class="track-artist">{artist_name_title}</div>
        </div>
        """, unsafe_allow_html=True)
        if pd.notna(recommendation['spotify_preview_url']):
            st.audio(recommendation['spotify_preview_url'])

    elif ind == 1:
        st.markdown(f"""
        <div class="track-card">
            <div class="track-badge up-next-badge">UP NEXT</div>
            <div class="track-title">{song_name_title}</div>
            <div class="track-artist">{artist_name_title}</div>
        </div>
        """, unsafe_allow_html=True)
        if pd.notna(recommendation['spotify_preview_url']):
            st.audio(recommendation['spotify_preview_url'])

    else:
        st.markdown(f"""
        <div class="track-card">
            <div class="track-number">{ind}</div>
            <div class="track-title">{song_name_title}</div>
            <div class="track-artist">{artist_name_title}</div>
        </div>
        """, unsafe_allow_html=True)
        if pd.notna(recommendation['spotify_preview_url']):
            st.audio(recommendation['spotify_preview_url'])


if filtering_type == 'content-based filtering':
    if st.button('Get Recommendation'):
        if ((st.session_state.data['artist'].str.lower() == artist_name) & (st.session_state.data['name'].str.lower() == song_name)).any():
            st.markdown(f"#### Recommendations for **{song_name.title()}**")

            recommendations = recommend(song_name, artist_name, st.session_state.data, st.session_state.transformed_data, k)

            if not recommendations.empty:
                for ind, recommendation in recommendations.iterrows():
                    render_song_card(recommendation, ind)
            else:
                st.info("No recommendations found for this song.")
        else:
            st.warning(f"Sorry, we couldn't find '{song_name}' in the dataset. Please try another song")


elif filtering_type == 'collaborative filtering':

    if st.button('Get Recommendation'):
        if ((st.session_state.filtered_data['artist'].str.lower() == artist_name) & (st.session_state.filtered_data['name'].str.lower() == song_name)).any():
            st.markdown(f"#### Recommendations for **{song_name.title()}**")

            try:
                recommendations = collaborative_recommendation(song_name, artist_name, st.session_state.track_ids, st.session_state.filtered_data, st.session_state.interaction_matrix, k)
            except ValueError as e:
                st.write(str(e))
                recommendations = pd.DataFrame()

            if not recommendations.empty:
                for ind, recommendation in recommendations.iterrows():
                    render_song_card(recommendation, ind)
            else:
                st.info("No recommendations found for this song.")
        else:
            st.warning(f"Sorry, we couldn't find '{song_name}' in the dataset. Please try another song")


if filtering_type == 'Hybrid Recommender System':

    if st.button('Get Recommendation'):
        if ((st.session_state.filtered_data['artist'].str.lower() == artist_name) & (st.session_state.filtered_data['name'].str.lower() == song_name)).any():
            st.markdown(f"#### Recommendations for **{song_name.title()}**")

            try:
                recommender = hrs(k, content_based_weight)
                recommendations = recommender.give_recommendations(song_name, artist_name, st.session_state.filtered_data, st.session_state.track_ids, st.session_state.transformed_hybrid_data, st.session_state.interaction_matrix)
            except ValueError as e:
                st.write("filtered_data shape:", st.session_state.filtered_data.shape)
                st.write("track_ids shape:", st.session_state.track_ids.shape)
                st.write("hybrid matrix shape:", st.session_state.transformed_hybrid_data.shape)
                st.write("interaction matrix shape:", st.session_state.interaction_matrix.shape)
                st.write("hybrid recommendation system failed")
                st.write(e)
                recommendations = pd.DataFrame()

            if not recommendations.empty:
                for ind, recommendation in recommendations.iterrows():
                    render_song_card(recommendation, ind)
            else:
                st.info("No recommendations found for this song.")
        else:
            st.warning(f"Sorry, we couldn't find '{song_name}' in the dataset. Please try another song")
    
