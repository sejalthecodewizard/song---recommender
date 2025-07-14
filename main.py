import streamlit as st
import pandas as pd
import time

# --- Custom CSS ---
st.markdown(
    """
    <style>
    .main { background-color: #fff94f; color: #333; }
    .floating-emojis { position: relative; height: 60px; margin-bottom: 20px; }
    .emoji { font-size: 2rem; position: absolute; animation: floatUp 4s ease-in-out infinite; user-select: none; }
    .emoji1 { left: 10%; animation-delay: 0s; }
    .emoji2 { left: 25%; animation-delay: 1s; }
    .emoji3 { left: 40%; animation-delay: 2s; }
    .emoji4 { left: 55%; animation-delay: 1.5s; }
    .emoji5 { left: 70%; animation-delay: 0.5s; }
    .emoji6 { left: 85%; animation-delay: 2.5s; }
    @keyframes floatUp {
        0% { transform: translateY(0); opacity: 1; }
        50% { transform: translateY(-20px); opacity: 0.8; }
        100% { transform: translateY(0); opacity: 1; }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Load Data safely (no genre required) ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("spotify.csv")
        df.columns = df.columns.str.strip().str.lower()
        required_cols = {'track_name', 'artist'}  # ✅ no genre!
        missing = required_cols - set(df.columns)
        if missing:
            st.error(f"Dataset missing columns: {', '.join(missing)}")
            return pd.DataFrame()
        return df
    except Exception as e:
        st.error("Error loading dataset.")
        st.write(e)
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.stop()

st.title("🎧 Moodify — Your AI Music Companion")

# --- Emojis ---
st.markdown("""
<div class="floating-emojis">
    <span class="emoji emoji1">😊</span>
    <span class="emoji emoji2">😢</span>
    <span class="emoji emoji3">😎</span>
    <span class="emoji emoji4">⚡</span>
    <span class="emoji emoji5">💕</span>
    <span class="emoji emoji6">🕵‍♂</span>
</div>
""", unsafe_allow_html=True)

# --- Moods ---
mood_options = {
    "Happy 😊": ["happy", "joy", "bright"],
    "Sad 😢": ["sad", "blue", "melancholy"],
    "Chill 😎": ["chill", "relax", "calm"],
    "Energetic ⚡": ["energetic", "upbeat", "fast"],
    "Romantic 💕": ["romantic", "love", "soft"],
    "Mysterious 🕵‍♂": ["mysterious", "dark", "moody"],
}

# --- Sidebar mood picker only ---
st.sidebar.header("🎶 Customize Your Vibe")
selected_mood = st.sidebar.selectbox("Select Mood", list(mood_options.keys()))

# --- Filter helper ---
def filter_by_mood(df, keywords):
    if "track_name" not in df.columns:
        return pd.DataFrame()
    return df[df["track_name"].str.contains('|'.join(keywords), case=False, na=False)]

# --- Filter songs ---
try:
    filtered = filter_by_mood(df, mood_options[selected_mood])
except Exception as e:
    st.error("Error filtering songs.")
    st.write(e)
    filtered = pd.DataFrame()

# --- Display results ---
st.markdown(f"### 🎶 Songs for {selected_mood}")
if filtered.empty:
    st.warning("No songs found! Here's a surprise instead:")
    try:
        surprise = df.sample(1).iloc[0]
        st.write(f"🎵 {surprise['track_name']} by {surprise['artist']}")
    except:
        st.error("No songs available to show.")
else:
    for _, row in filtered.sample(min(5, len(filtered))).iterrows():
        st.write(f"🎵 {row['track_name']} by {row['artist']}")

# --- Mystery Box ---
st.markdown("---")
st.header("🎁 Mystery Box — Get a surprise song!")

if 'mystery_opened' not in st.session_state:
    st.session_state.mystery_opened = False

if st.button("Open Mystery Box"):
    if not st.session_state.mystery_opened:
        st.session_state.mystery_opened = True
        with st.spinner("Opening the box..."):
            time.sleep(2)
        mystery = df.sample(1).iloc[0]
        st.balloons()
        st.success(f"✨ You got: 🎶 {mystery['track_name']} by {mystery['artist']} ✨")
    else:
        st.info("Already opened! Refresh to try again.")

if st.button("🔄 Reset Mystery Box"):
    st.session_state.mystery_opened = False
    st.info("Box reset! You can open it again.")
        
   

       
   
   


    
      


   
   
  

   
       
    


