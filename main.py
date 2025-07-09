import streamlit as st
import pandas as pd

# Load data from CSV file
@st.cache_data
def load_data():
    df = pd.read_csv("spotify.csv")
    return df

df = load_data()

st.title("🎧 Mood-Based Spotify Song Recommender")

# Mood options
mood = st.selectbox("Pick your mood:", ["Happy", "Sad", "Energetic", "Calm"])

# Mood logic — uses valence & energy to filter
if mood == "Happy":
    filtered = df[df["valence"] > 0.7]
elif mood == "Sad":
    filtered = df[df["valence"] < 0.3]
elif mood == "Energetic":
    filtered = df[df["energy"] > 0.7]
else:  # Calm
    filtered = df[(df["energy"] < 0.4) & (df["valence"] > 0.5)]

# Show 5 recommendations
st.markdown("### ✨ Your recommended songs:")
for i, row in filtered.sample(5).iterrows():
    st.write(f"🎵 *{row['track_name']}* by {row['artist_name']}")

# 🎁 Mystery Box
st.markdown("---")
st.header("🎁 Mystery Box — Get a surprise song!")

if st.button("Open Mystery Box"):
    mystery = df.sample(1).iloc[0]
    st.success(f"🎶 *{mystery['track_name']}* by {mystery['artist_name']}")
