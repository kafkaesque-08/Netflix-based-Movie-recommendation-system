import streamlit as st
import pickle
import pandas as pd
import requests
from urllib.parse import quote

# ================== PAGE CONFIG ==================
st.set_page_config(
    page_title="Netflix-Style Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

# ================== NETFLIX STYLE CSS ==================
st.markdown("""
<style>
body {
    background-color: #141414;
    color: white;
}

h1, h2, h3 {
    color: #E50914;
}

.movie-card {
    background-color: #1f1f1f;
    padding: 10px;
    border-radius: 10px;
    text-align: center;
}

.movie-card img {
    border-radius: 8px;
}

.stButton>button {
    background-color: #E50914;
    color: white;
    border-radius: 8px;
    border: none;
    padding: 0.6rem 1.2rem;
    font-weight: bold;
}

.stButton>button:hover {
    background-color: #f40612;
}
</style>
""", unsafe_allow_html=True)

# ================== TITLE ==================
st.markdown("<h1>🎬 Netflix-Style Movie Recommender</h1>", unsafe_allow_html=True)
st.write("Search a movie and get recommendations instantly")

# ================== OMDb API KEY ==================
OMDB_API_KEY = "b19c639e"

# ================== LOAD DATA ==================
@st.cache_data
def load_data():
    movies = pickle.load(open("movies_rec.pkl", "rb"))
    similarity = pickle.load(open("similarity.pkl", "rb"))
    return movies, similarity

movies, similarity = load_data()

# ================== FETCH POSTER ==================
@st.cache_data
def fetch_poster(title):
    safe_title = quote(title)
    url = f"http://www.omdbapi.com/?t={safe_title}&apikey={OMDB_API_KEY}"
    data = requests.get(url, timeout=5).json()

    if data.get("Response") == "True" and data.get("Poster") != "N/A":
        return data["Poster"]
    return "https://via.placeholder.com/300x450?text=No+Poster"

# ================== RECOMMEND FUNCTION ==================
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:11]

    results = []
    for i in movies_list:
        title = movies.iloc[i[0]].title
        poster = fetch_poster(title)
        results.append((title, poster))

    return results

# ================== SEARCH UI ==================
search_query = st.text_input("🔍 Search for a movie")

filtered_movies = movies[movies['title'].str.contains(
    search_query, case=False, na=False
)] if search_query else movies

selected_movie = st.selectbox(
    "🎥 Select a movie",
    filtered_movies['title'].values
)

# ================== BUTTON ==================
if st.button("🚀 Recommend"):
    recommendations = recommend(selected_movie)

    st.markdown("<h2>✨ Recommended for You</h2>", unsafe_allow_html=True)

    cols = st.columns(5)
    for idx, (title, poster) in enumerate(recommendations):
        with cols[idx % 5]:
            st.markdown('<div class="movie-card">', unsafe_allow_html=True)
            st.image(poster, use_container_width=True)
            st.caption(title)
            st.markdown('</div>', unsafe_allow_html=True)

# ================== FOOTER ==================
st.markdown("---")
st.caption("Built with ❤️ using Streamlit | Netflix-style UI | OMDb API")
