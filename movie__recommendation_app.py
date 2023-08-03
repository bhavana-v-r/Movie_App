
from pickle5 import pickle
import pandas as pd
import streamlit as st
from streamlit import session_state as session
from sklearn.metrics.pairwise import cosine_similarity


# in this function, the tfidf dataframe is loaded and after that, it stored as a cache
@st.cache(persist=True, show_spinner=False,
suppress_st_warning=True)
def recommend_table(list_of_movie_enjoyed,tfidf_data, movie_count=20):
    """
    function for recommending movies
    :param list_of_movie_enjoyed: list of movies
    :param tfidf_data: self-explanatory
    :param movie_count: no of movies to suggest
    :return: dataframe containing suggested movie
    """
    movie_enjoyed_df = tfidf_data.reindex(list_of_movie_enjoyed)
    user_prof = movie_enjoyed_df.mean()
    tfidf_subset_df = tfidf_data.drop(list_of_movie_enjoyed)
    similarity_array = cosine_similarity(user_prof.values.reshape(1, -1), tfidf_subset_df)
    similarity_df = pd.DataFrame(similarity_array.T,
    index=tfidf_subset_df.index,
    columns=["similarity_score"])
    sorted_similarity_df = similarity_df.sort_values(by="similarity_score", ascending=False).head(movie_count)
    return sorted_similarity_df
def load_data():
    """
    load and cache data
    :return: tfidf data
    """
    tfidf_data = pd.read_csv("tfidf_small_df.csv", index_col=0)
    return tfidf_data


tfidf = load_data()

with open("movie_list_small.pickle", "rb") as f:
movies = pickle.load(f)

dataframe = None

st.title("""
Netflix Recommendation System
This is an Content Based Recommender System made on implicit ratings :smile:.
""")

st.text("")
st.text("")
st.text("")
st.text("")

session.options = st.multiselect(label="Select Movies", options=movies)

st.text("")
st.text("")

session.slider_count = st.slider(label="movie_count", min_value=5, max_value=50)

st.text("")
st.text("")

buffer1, col1, buffer2 = st.columns([1.45, 1, 1])

is_clicked = col1.button(label="Recommend")

if is_clicked:
    dataframe = recommend_table(session.options, movie_count=session.slider_count, tfidf_data=tfidf)

st.text("")
st.text("")
st.text("")
st.text("")

if dataframe is not None:
    st.table(dataframe)
