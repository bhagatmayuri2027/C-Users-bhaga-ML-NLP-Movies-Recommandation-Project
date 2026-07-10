import pandas as pd
import streamlit as st
import pickle
import gzip
import os
import gdown

if not os.path.exists("similarity.pkl.gz"):
    file_id = "1Id6A_vlSICIk7xgz0aaom16ypOc42T8z"
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, "similarity.pkl.gz", quiet=False)

with gzip.open("similarity.pkl.gz", "rb") as f:
    similarity = pickle.load(f)

st.title("Movie Recommender System")
df = pd.read_csv('cleaned_data.csv')


movies = df['title'].tolist()

name = st.selectbox("Select a movie", movies)

# def get_movie_index(name):
#     index = -1
#     for i in df.index:
#         if df.loc[i, "title"] == name:
#             index = i
#             break
#     return index    

#Lets write function get name of movie by index
def get_name_by_index(i):
    if 0 <= i < len(df):
        return df.loc[i, "title"]
    return ""

def get_index_from_name(name):

    clean_user_name = str(name).strip().lower().replace(' ', '').replace('-', '')

    clean_titles = (
        df['title']
        .fillna('')
        .astype(str)
        .str.lower()
        .str.replace(' ', '', regex=False)
        .str.replace('-', '', regex=False)
    )

    match = df[clean_titles == clean_user_name]

    if not match.empty:
        return match.index[0]

    return -1

# def get_movie_title(i):
#     if i > len(df):
#         return ""
#     else:
#         return df.loc[i, 'title']

if st.button("Recommend"):
    index = get_index_from_name(name)

    if index == -1:
        st.write("Movie not found.")
    else:
        similarity_indexes = list(enumerate(similarity[index]))
        similarity_indexes = sorted(
            similarity_indexes,
            key=lambda x: x[1],
            reverse=True
        )

        st.subheader("Recommended Movies")

        for i in range(1, 6):
            st.write(f"{i}. {get_name_by_index(similarity_indexes[i][0])}")