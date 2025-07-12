import streamlit as st
import pandas as pd

# Clean and load the dataset
@st.cache_data
def load_data():
    df = pd.read_csv("spotify.csv")
    df.columns = df.columns.str.strip().str.lower()  # clean column names
    return df

df = load_data()

st.title("🎧 Spotify Song Recommender")

# Mood filter based on columns that exist in your CSV
mood = st.selectbox("Pick your mood:", ["Popular", "Long Songs", "Short Songs", "Random"])

if mood == "Popular":
    filtered = df[df["popularity"] > 85]
elif mood == "Long Songs":
    filtered = df[df["duration_min"] > 4]
elif mood == "Short Songs":
    filtered = df[df["duration_min"] < 3]
else:
    filtered = df.sample(5)

st.markdown("### ✨ Your recommended songs:")
if not filtered.empty:
    for i, row in filtered.iterrows():
        st.write(f"🎵 {row['track_name']} by {row['artist']}")
else:
    st.warning("😕 No songs match this mood in your dataset.")

# 🎁 Mystery Box
st.markdown("---")
st.header("🎁 Mystery Box — Get a surprise song!")

if st.button("Open Mystery Box"):
    mystery = df.sample(1).iloc[0]
    st.success(f"🎶 {mystery['track_name']} by {mystery['artist']}")
