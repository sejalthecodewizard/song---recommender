import streamlit as st
import pandas as pd
import random
import time

# --- Custom CSS for bright yellow background and floating emojis ---
st.markdown(
    """
    <style>
    /* Bright yellow background */
    .main {
        background-color: #fff94f;
        color: #333333;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Floating emojis container */
    .floating-emojis {
        position: relative;
        width: 100%;
        height: 60px;
        margin-bottom: 20px;
    }

    /* Individual emoji style */
    .emoji {
        font-size: 2rem;
        position: absolute;
        animation-name: floatUp;
        animation-timing-function: ease-in-out;
        animation-iteration-count: infinite;
        animation-duration: 4s;
        user-select: none;
    }

    /* Different delays and positions for each emoji */
    .emoji1 { left: 10%; animation-delay: 0s; }
    .emoji2 { left: 25%; animation-delay: 1s; }
    .emoji3 { left: 40%; animation-delay: 2s; }
    .emoji4 { left: 55%; animation-delay: 1.5s; }
    .emoji5 { left: 70%; animation-delay: 0.5s; }
    .emoji6 { left: 85%; animation-delay: 2.5s; }

    /* Float animation */
    @keyframes floatUp {
        0% { transform: translateY(0); opacity: 1; }
        50% { transform: translateY(-20px); opacity: 0.8; }
        100% { transform: translateY(0); opacity: 1; }
    }

    /* Big mystery box button style */
    .mystery-button {
        font-size: 1.5rem;
        padding: 20px 40px;
        background-color: #ffdd57;
        border: none;
        border-radius: 25px;
        cursor: pointer;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        transition: background-color 0.3s ease;
        width: 100%;
        max-width: 400px;
        margin: 20px auto;
        display: block;
    }
    .mystery-button:hover {
        background-color: #ffe87f;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv("spotify.csv")
    df.columns = df.columns.str.strip().str.lower()
    return df

df = load_data()

# --- Title ---
st.title("🎧 Moodify — Your AI Music Companion")

# --- Floating emojis for emotions ---
st.markdown(
    """
    <div class="floating-emojis" aria-label="Floating mood emojis">
        <span class="emoji emoji1" title="Happy">😊</span>
        <span class="emoji emoji2" title="Sad">😢</span>
        <span class="emoji emoji3" title="Chill">😎</span>
        <span class="emoji emoji4" title="Energetic">⚡</span>
        <span class="emoji emoji5" title="Romantic">💕</span>
        <span class="emoji emoji6" title="Mysterious">🕵‍♂</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- Mood Selector with emojis below ---
mood_options = {
    "Happy 😊": ["happy", "joy", "bright"],
    "Sad 😢": ["sad", "blue", "melancholy"],
    "Chill 😎": ["chill", "relax", "calm"],
    "Energetic ⚡": ["energetic", "upbeat", "fast"],
    "Romantic 💕": ["romantic", "love", "soft"],
    "Mysterious 🕵‍♂": ["mysterious", "dark", "moody"],
}

selected_mood = st.selectbox("Select your mood to find songs:", list(mood_options.keys()))

def filter_by_mood(df, keywords):
    mask = df['track_name'].str.contains('|'.join(keywords), case=False, na=False)
    return df[mask]

filtered_songs = filter_by_mood(df, mood_options[selected_mood])

st.markdown(f"### 🎶 Songs for {selected_mood}")

if filtered_songs.empty:
    st.warning("No songs found for this mood! Here's a surprise:")
    surprise = df.sample(1).iloc[0]
    st.write(f"🎵 {surprise['track_name']} by {surprise['artist']}")
else:
    sample_songs = filtered_songs.sample(min(5, len(filtered_songs)))
    for _, row in sample_songs.iterrows():
        st.write(f"🎵 {row['track_name']} by {row['artist']}")

st.markdown("---")

# --- Mystery Box with “Subway Surfers item drop” feel ---
st.header("🎁 Mystery Box — Open to get a surprise song!")

if st.button("Open Mystery Box", key="mystery"):
    with st.spinner('Opening Mystery Box... 🎲🎵'):
        time.sleep(3)  # simulate suspense
    mystery_song = df.sample(1).iloc[0]
    st.balloons()
    st.success(f"✨ You got: 🎶 {mystery_song['track_name']} by {mystery_song['artist']} ✨")
