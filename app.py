import streamlit as st
import pickle
import pandas as pd
import requests
from dotenv import load_dotenv
import os
load_dotenv()
API_KEY=os.getenv("TMDB_API_KEY")

def fetch_poster(movie_id):
    url=f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=API_KEY'
    try:
        response=requests.get(url,timeout=10)
        response.raise_for_status()
        data=response.json()

        if data.get("poster_path"):
            return "https://image.tmdb.org/t/p/w500/"+data['poster_path']
    except requests.exceptions.RequestException as e:
        print("API ERROR ",e)

    return "https://via.placeholder.com/500x750?text=No+Postser"
def recommend(movie_name):
    movie_index=movies[movies['title']==movie_name].index[0]
    movies_list=similarity[movie_index]
    # movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    recommended_movie=[]
    recommended_movie_posters=[]
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        #fetch poster from api



        recommended_movie.append(movies.iloc[i[0]].title)
        # fetch poster from api
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movie,recommended_movie_posters
movies_dict=pickle.load(open("movies_dict.pkl","rb"))
similarity=pickle.load(open("reduced_similarity.pkl","rb"))


movies=pd.DataFrame(movies_dict)

st.title("Movie Recommender System")
selected_movie_name=st.selectbox(
    "Select Movie",
    movies['title'].values)


if st.button("Recommend"):
    names,posters=recommend(selected_movie_name)
    col1,col2,col3,col4,col5=st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])


    # st.write(selected_movie_name)