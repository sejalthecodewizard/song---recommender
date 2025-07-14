import streamlit as st
import pandas as pd
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

# --- Load Data safely ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("spotify.csv")
        df.columns = df.columns.str.strip().str.lower()
        # Check required columns exist, except genre is optional now
        required_cols = {'track_name', 'artist'}
        missing_cols = required_cols - set(df.columns)
        if missing_cols:
            st.error(f"Dataset missing columns: {', '.join(missing_cols)}")
            return pd.DataFrame()  # Return empty df to prevent errors
        return df
    except Exception as e:
        st.error("Error loading data. Please check 'spotify.csv'.")
        st.write(e)
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.stop()  # Stop further app execution if dataset invalid

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

# --- Mood Options with keywords ---
mood_options = {
    "Happy 😊": ["happy", "joy", "bright"],
    "Sad 😢": ["sad", "blue", "melancholy"],
    "Chill 😎": ["chill", "relax", "calm"],
    "Energetic ⚡": ["energetic", "upbeat", "fast"],
    "Romantic 💕": ["romantic", "love", "soft"],
    "Mysterious 🕵‍♂": ["mysterious", "dark", "moody"],
}

# --- Genre Options removed since dataset has no genre ---
# So no genre selection UI or filtering

# --- Sidebar selectors ---
st.sidebar.header("🎶 Customize Your Vibe")

selected_mood = st.sidebar.selectbox("Select Mood", list(mood_options.keys()))

# --- Filtering helper function ---
def filter_by_mood(dataframe, keywords):
    if 'track_name' not in dataframe.columns:
        return pd.DataFrame()
    mask = dataframe['track_name'].str.contains('|'.join(keywords), case=False, na=False)
    return dataframe[mask]

# --- Filter songs ---
try:
    filtered_songs = filter_by_mood(df, mood_options[selected_mood])
except Exception as e:
    st.error("Error filtering songs.")
    st.write(e)
    filtered_songs = pd.DataFrame()

# --- Display songs ---
st.markdown(f"### 🎶 Songs for {selected_mood}")

if filtered_songs.empty:
    st.warning("No songs found for your vibe! Here's a surprise:")
    try:
        surprise = df.sample(1).iloc[0]
        st.write(f"🎵 {surprise['track_name']} by {surprise['artist']}")
    except Exception as e:
        st.error("No songs available to show.")
        st.write(e)
else:
    sample_songs = filtered_songs.sample(min(5, len(filtered_songs)))
    for _, row in sample_songs.iterrows():
        track = row.get('track_name', 'Unknown Track')
        artist = row.get('artist', 'Unknown Artist')
        st.write(f"🎵 {track} by {artist}")

st.markdown("---")

# --- Mystery Box with session state to avoid multiple clicks ---
st.header("🎁 Mystery Box — Open to get a surprise song!")

if 'mystery_opened' not in st.session_state:
    st.session_state.mystery_opened = False

if st.button("Open Mystery Box", key="mystery"):
    if not st.session_state.mystery_opened:
        st.session_state.mystery_opened = True
        with st.spinner('Opening Mystery Box... 🎲🎵'):
            time.sleep(3)  # suspense effect
        try:
            mystery_song = df.sample(1).iloc[0]
            st.balloons()
            track = mystery_song.get('track_name', 'Unknown Track')
            artist = mystery_song.get('artist', 'Unknown Artist')
            st.success(f"✨ You got: 🎶 {track} by {artist} ✨")
        except Exception as e:
            st.error("Failed to get a mystery song.")
            st.write(e)
    else:
        st.info("You already opened the Mystery Box! Refresh the page to open again.")

# --- Reset Mystery Box Button ---
if st.button("Reset Mystery Box"):
    st.session_state.mystery_opened = False
    st.info("Mystery Box is reset. You can open it again!")

# You can continue adding your other features here safely following these patterns...
    
       


   
   
  

   
       
    


