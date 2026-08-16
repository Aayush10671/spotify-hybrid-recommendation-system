FROM python:3.12-slim

WORKDIR /app/

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./data/collab_filtered_data.csv \ 
    ./data/interaction_matrix.npz \
    ./data/track_ids.npy \
    ./data/cleaned_data.csv \
    ./data/transformed_data.npz \
    ./data/transformed_hybrid_data.npz \
    ./data/

COPY app.py \
    collaborative_filtering.py \
    content_based_filtering.py \
    hybrid_recommendation.py \
    data_cleaning.py \
    transform_filter_data.py \
    ./

EXPOSE 8000


CMD ["streamlit","run","app.py","--server.port","8000"]
