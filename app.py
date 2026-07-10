import pandas as pd
import streamlit as st
import pickle
import gzip

st.title("Movie Recommender System")

# Load dataset
df = pd.read_csv("cleaned_data.csv")

# Load compressed similarity matrix
with gzip.open("similarity.pkl.gz", "rb") as f:
    similarity = pickle.load(f)

movies = df['title'].tolist()

name = st.selectbox("Select a movie", movies)


# Get movie name by index
def get_name_by_index(i):
    if 0 <= i < len(df):
        return df.loc[i, 'title']
    else:
        return ""


# Get index from movie name
def get_index_from_name(name):
    clean_user_name = name.strip().lower().replace(" ", "").replace("-", "")

    match = df[
        df["title"]
        .str.lower()
        .str.replace(" ", "", regex=False)
        .str.replace("-", "", regex=False)
        == clean_user_name
    ]

    if not match.empty:
        return match.index[0]
    return -1


if st.button("Recommend"):

    index = get_index_from_name(name)

    if index == -1:
        st.error("Movie not found. Please check the spelling and try again.")

    else:
        st.subheader(f"Recommendations for '{name}'")

        similarity_indexes = list(enumerate(similarity[index]))
        similarity_indexes = sorted(
            similarity_indexes,
            key=lambda x: x[1],
            reverse=True
        )

        for i in range(1, 6):
            movie_index = similarity_indexes[i][0]
            st.write(f"{i}. {get_name_by_index(movie_index)}")
