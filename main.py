import streamlit as st
import pandas as pd

# Cache data loading to speed up app
@st.cache_data
def load_data():
    df = pd.read_csv("spotify.csv")
    df.columns = df.columns.str.strip().str.lower()  # clean column names
    return df

df = load_data()

st.title("🎧 Spotify Song Recommender")

# Mood filter dropdown
mood = st.selectbox("Pick your mood:", ["Popular", "Long Songs", "Short Songs", "Random"])

# Filter songs based on mood
if mood == "Popular":
    filtered = df[df["popularity"] > 85]
elif mood == "Long Songs":
    filtered = df[df["duration_min"] > 4]
elif mood == "Short Songs":
    filtered = df[df["duration_min"] < 3]
else:  # Random
    filtered = df.sample(5)

st.markdown("### ✨ Your recommended songs:")
if not filtered.empty:
    # Show up to 5 songs for Popular, Long, and Short moods
    if mood != "Random":
        filtered = filtered.sample(min(5, len(filtered)))
    for _, row in filtered.iterrows():
        st.write(f"🎵 {row['track_name']} by {row['artist']}")
else:
    st.warning("😕 No songs match this mood in your dataset.")

# 🎁 Mystery Box feature
st.markdown("---")
st.header("🎁 Mystery Box — Get a surprise song!")

if st.button("Open Mystery Box"):
    mystery = df.sample(1).iloc[0]
    st.success(f"🎶 {mystery['track_name']} by {mystery['artist']}")
