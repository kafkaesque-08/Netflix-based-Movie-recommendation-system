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
/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Dark background like Netflix */
.stApp {
    background: linear-gradient(180deg, #141414 0%, #000000 100%);
}

/* Main container styling */
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1400px;
}

/* Netflix logo-style title */
.netflix-title {
    font-family: 'Bebas Neue', 'Arial Black', sans-serif;
    font-size: 3.5rem;
    font-weight: 900;
    color: #E50914;
    text-shadow: 2px 2px 8px rgba(229, 9, 20, 0.5);
    letter-spacing: 2px;
    margin-bottom: 0;
}

.subtitle {
    color: #808080;
    font-size: 1.1rem;
    margin-top: 0;
    margin-bottom: 2rem;
}

/* Section headers */
h2 {
    color: #FFFFFF !important;
    font-weight: 700;
    font-size: 1.5rem;
    margin-top: 2rem;
    padding-left: 0.5rem;
    border-left: 4px solid #E50914;
}

/* Search input styling */
.stTextInput > div > div > input {
    background-color: #333333;
    color: white;
    border: 2px solid #444444;
    border-radius: 4px;
    padding: 12px 16px;
    font-size: 1rem;
    transition: all 0.3s ease;
}

.stTextInput > div > div > input:focus {
    border-color: #E50914;
    box-shadow: 0 0 10px rgba(229, 9, 20, 0.3);
}

.stTextInput > div > div > input::placeholder {
    color: #888888;
}

/* Selectbox styling */
.stSelectbox > div > div {
    background-color: #333333;
    border: 2px solid #444444;
    border-radius: 4px;
}

.stSelectbox > div > div:hover {
    border-color: #E50914;
}

/* Button styling */
.stButton > button {
    background: linear-gradient(180deg, #E50914 0%, #B20710 100%);
    color: white;
    border: none;
    border-radius: 4px;
    padding: 0.75rem 2rem;
    font-size: 1rem;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(229, 9, 20, 0.4);
    width: 100%;
    margin-top: 1rem;
}

.stButton > button:hover {
    background: linear-gradient(180deg, #F40612 0%, #E50914 100%);
    box-shadow: 0 6px 20px rgba(229, 9, 20, 0.6);
    transform: translateY(-2px);
}

.stButton > button:active {
    transform: translateY(0);
}

/* Movie card styling */
.movie-card {
    background: linear-gradient(145deg, #1a1a1a 0%, #0d0d0d 100%);
    border-radius: 8px;
    padding: 12px;
    margin: 8px 0;
    transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    border: 1px solid #2a2a2a;
    position: relative;
    overflow: hidden;
}

.movie-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, #E50914, #FF6B6B, #E50914);
    opacity: 0;
    transition: opacity 0.3s ease;
}

.movie-card:hover {
    transform: scale(1.05);
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.8), 0 0 20px rgba(229, 9, 20, 0.2);
    border-color: #E50914;
    z-index: 10;
}

.movie-card:hover::before {
    opacity: 1;
}

.movie-title {
    color: #FFFFFF;
    font-size: 0.9rem;
    font-weight: 600;
    margin-top: 10px;
    text-align: center;
    line-height: 1.3;
}

/* Image styling */
.movie-card img {
    border-radius: 4px;
    width: 100%;
    aspect-ratio: 2/3;
    object-fit: cover;
}

/* Caption styling */
.stCaption {
    color: #CCCCCC !important;
    font-weight: 500;
}

/* Divider */
hr {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, #333333, transparent);
    margin: 2rem 0;
}

/* Footer styling */
.footer {
    text-align: center;
    color: #666666;
    font-size: 0.85rem;
    padding: 2rem 0;
}

.footer a {
    color: #E50914;
    text-decoration: none;
}

/* Label styling */
.stTextInput label, .stSelectbox label {
    color: #FFFFFF !important;
    font-weight: 600;
    font-size: 0.9rem;
    margin-bottom: 0.5rem;
}

/* Top 10 badge */
.top-badge {
    background: linear-gradient(135deg, #E50914, #B20710);
    color: white;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 0.7rem;
    font-weight: 700;
    position: absolute;
    top: 8px;
    left: 8px;
    z-index: 5;
}

/* Scrollbar styling */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: #141414;
}

::-webkit-scrollbar-thumb {
    background: #E50914;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: #F40612;
}

/* Loading animation */
.stSpinner > div {
    border-top-color: #E50914 !important;
}
</style>

<!-- Google Font for Netflix-style title -->
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# ================== TITLE ==================
st.markdown("""
<div style="text-align: center; padding: 1rem 0 2rem 0;">
    <h1 class="netflix-title">MOVIEFLIX</h1>
    <p class="subtitle">Discover your next favorite movie with AI-powered recommendations</p>
</div>
""", unsafe_allow_html=True)

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
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    search_query = st.text_input("", placeholder="Search for a movie...")

    filtered_movies = movies[movies['title'].str.contains(
        search_query, case=False, na=False
    )] if search_query else movies

    selected_movie = st.selectbox(
        "Select a movie",
        filtered_movies['title'].values,
        label_visibility="collapsed"
    )

    # ================== BUTTON ==================
    recommend_clicked = st.button("Get Recommendations")

# ================== RECOMMENDATIONS ==================
if recommend_clicked:
    with st.spinner("Finding perfect matches..."):
        recommendations = recommend(selected_movie)

    st.markdown("""
    <h2 style="margin-top: 3rem;">Because you liked "{}"</h2>
    """.format(selected_movie), unsafe_allow_html=True)

    # First row (5 movies)
    cols = st.columns(5, gap="medium")
    for idx, (title, poster) in enumerate(recommendations[:5]):
        with cols[idx]:
            st.markdown(f"""
            <div class="movie-card">
                <span class="top-badge">TOP {idx + 1}</span>
                <img src="{poster}" alt="{title}">
                <p class="movie-title">{title}</p>
            </div>
            """, unsafe_allow_html=True)

    # Second row (5 movies)
    cols2 = st.columns(5, gap="medium")
    for idx, (title, poster) in enumerate(recommendations[5:]):
        with cols2[idx]:
            st.markdown(f"""
            <div class="movie-card">
                <span class="top-badge">TOP {idx + 6}</span>
                <img src="{poster}" alt="{title}">
                <p class="movie-title">{title}</p>
            </div>
            """, unsafe_allow_html=True)

# ================== FOOTER ==================
st.markdown("""
<div class="footer">
    <hr>
    <p>Built with Streamlit | Powered by OMDb API</p>
    <p style="color: #E50914; font-weight: 600;">MOVIEFLIX</p>
</div>
""", unsafe_allow_html=True)
