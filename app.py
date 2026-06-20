import streamlit as st
import pickle
import pandas as pd
import requests

# Load TMDB API Key from Streamlit Secrets
API_KEY = st.secrets["TMDB_API_KEY"]


# Fetch movie poster from TMDB
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("poster_path"):
            return "https://image.tmdb.org/t/p/w500" + data["poster_path"]

    except requests.exceptions.RequestException as e:
        st.error(f"TMDB API Error: {e}")

    return "https://via.placeholder.com/500x750?text=No+Poster"


# Recommend movies
def recommend(movie_name):
    movie_index = movies[movies["title"] == movie_name].index[0]

    movies_list = similarity[movie_index]

    recommended_movies = []
    recommended_posters = []

    for item in movies_list:
        index = item[0]  # movie index from reduced_similarity

        movie_id = movies.iloc[index].movie_id

        recommended_movies.append(movies.iloc[index].title)

        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters


# Load data
with open("movies_dict.pkl", "rb") as file:
    movies_dict = pickle.load(file)

with open("reduced_similarity.pkl", "rb") as file:
    similarity = pickle.load(file)

movies = pd.DataFrame(movies_dict)


# Streamlit UI
st.title("🎬 Movie Recommender System ")

selected_movie_name = st.selectbox(
    "Select a Movie",
    movies["title"].values
)


if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    columns = [col1, col2, col3, col4, col5]

    for i in range(5):
        with columns[i]:
            st.text(names[i])
            st.image(posters[i], use_container_width=True)