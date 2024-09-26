import pickle
import streamlit as st
import requests
import certifi
import os
from dotenv import load_dotenv

load_dotenv()

api_key=os.getenv("API_KEY")

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key={API_KEY}&language=en-US".format(movie_id)
    data = requests.get(url, verify=certifi.where())  # Use certifi for SSL certificates
    data = data.json()
    poster_path = data['poster_path']
    if poster_path:
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    else:
        return "https://via.placeholder.com/500x750.png?text=No+Image"

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters


st.header('Movie Recommender System')
movies = pickle.load(open('D:/Movies/Project/movie-recommender-system-tmdb-dataset-main/movie_list.pkl', 'rb'))
similarity = pickle.load(open('D:/Movies/Project/movie-recommender-system-tmdb-dataset-main/similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    # Create 5 columns dynamically
    cols = st.columns(5)  # Replace st.beta_columns with st.columns

    for i, col in enumerate(cols):
        with col:
            st.text(recommended_movie_names[i])
            st.image(recommended_movie_posters[i])

