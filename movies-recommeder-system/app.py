import streamlit as st
import pickle
import pandas as pd
import requests

# Function to fetch the poster for a given movie ID
def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=0edd3538eeef07660b903de4544819dc&language=en-US'
    response = requests.get(url)
    data = response.json()

    # Debugging: Removed st.write statement
    # st.write(f"API response for movie ID {movie_id}: {data}")

    if 'poster_path' in data and data['poster_path']:
        return "http://image.tmdb.org/t/p/w500" + data['poster_path']
    else:
        return "https://via.placeholder.com/150"  # Placeholder image if poster_path is not available

# Function to recommend movies based on the selected movie
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_poster

# Load movies data and similarity matrix
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit application title
st.title('Movie Recommender System')

# Movie selection dropdown
selected_movie_name = st.selectbox('Choose a movie', movies['title'].values)

# Recommend button
if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    for idx, (name, poster) in enumerate(zip(names, posters)):
        with locals()[f'col{idx + 1}']:
            st.text(name)
            st.image(poster)
