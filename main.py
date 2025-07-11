import streamlit as st
import pandas as pd

# Clean and load the dataset
@st.cache_data
def load_data():
    df = pd.read_csv("spotify.csv")
    df.columns = df.columns.str.strip().str.lower()  # clean column names
    return df

df = load_data()

st.title("🎧 Mood-Based Spotify Song Recommender")

# Mood options
mood = st.selectbox("Pick your mood:", ["Happy", "Sad", "Energetic", "Calm"])

# Mood logic — uses valence & energy to filter
if "valence" in df.columns and "energy" in df.columns:
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
    if not filtered.empty:
        for i, row in filtered.sample(min(5, len(filtered))).iterrows():
            st.write(f"🎵 {row['track_name']} by {row['artist_name']}")
    else:
        st.warning("😕 No songs match this mood in your dataset.")
else:
    st.error("🚨 'valence' and/or 'energy' column not found in your dataset.")

# 🎁 Mystery Box
st.markdown("---")
st.header("🎁 Mystery Box — Get a surprise song!")

if st.button("Open Mystery Box"):
    mystery = df.sample(1).iloc[0]
    st.success(f"🎶 {mystery['track_name']} by {mystery['artist_name']}")
