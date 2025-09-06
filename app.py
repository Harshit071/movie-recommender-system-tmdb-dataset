import os
import pickle
import streamlit as st
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

def _normalize_text_series(series):
    series = series.fillna("")
    return series.astype(str)

def recommend(movie, movies_df, similarity_matrix):
    index = movies_df[movies_df['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity_matrix[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    for i in distances[1:6]:
        recommended_movie_names.append(movies_df.iloc[i[0]].title)

    return recommended_movie_names


st.header('Movie Recommender System')

# Load models with graceful error handling
@st.cache_resource(show_spinner=True)
def load_or_build_model():
    os.makedirs('model', exist_ok=True)
    movie_pkl = 'model/movie_list.pkl'
    sim_pkl = 'model/similarity.pkl'
    if os.path.exists(movie_pkl) and os.path.exists(sim_pkl):
        try:
            with open(movie_pkl, 'rb') as f:
                movies_df = pickle.load(f)
            with open(sim_pkl, 'rb') as f:
                similarity_matrix = pickle.load(f)
            # Basic validation
            if 'title' in movies_df.columns and len(movies_df) == np.array(similarity_matrix).shape[0] == np.array(similarity_matrix).shape[1]:
                # If artifacts look suspiciously small, prefer rebuilding from CSV if available
                if len(movies_df) < 1000 and os.path.exists('tmdb_5000_movies.csv'):
                    pass
                else:
                    return movies_df, similarity_matrix
        except Exception:
            pass

    # Build from CSVs (no posters, overview-only TF-IDF)
    movies_csv = 'tmdb_5000_movies.csv'
    if not os.path.exists(movies_csv):
        st.error('Missing dataset file: {}'.format(movies_csv))
        st.stop()
    movies_raw = pd.read_csv(movies_csv)
    # Use id as movie_id and ensure title exists
    if 'id' not in movies_raw.columns or 'title' not in movies_raw.columns:
        st.error('The movies CSV must have columns `id` and `title`.')
        st.stop()
    movies_df = movies_raw[['id', 'title', 'overview']].rename(columns={'id': 'movie_id'})
    movies_df['overview'] = _normalize_text_series(movies_df.get('overview'))

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf = vectorizer.fit_transform(movies_df['overview'])
    similarity_matrix = linear_kernel(tfidf, tfidf)

    # Persist for subsequent runs
    with open(movie_pkl, 'wb') as f:
        pickle.dump(movies_df[['movie_id', 'title']], f)
    with open(sim_pkl, 'wb') as f:
        pickle.dump(similarity_matrix, f)

    return movies_df[['movie_id', 'title']], similarity_matrix

movies, similarity = load_or_build_model()

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names = recommend(selected_movie, movies, similarity)
    num_to_show = min(5, len(recommended_movie_names))
    if num_to_show == 0:
        st.info("No recommendations found.")
    else:
        cols = st.columns(num_to_show)
        for idx in range(num_to_show):
            with cols[idx]:
                st.text(recommended_movie_names[idx])





