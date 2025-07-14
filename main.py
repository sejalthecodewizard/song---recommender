import streamlit as st
import pandas as pd
import time

# --- Custom CSS for bright yellow Moodify UI ---
st.markdown(
    """
    <style>
    .main { background-color: #fff94f; color: #333333; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .floating-emojis {
        position: relative; width: 100%; height: 60px; margin-bottom: 20px;
    }
    .emoji {
        font-size: 2rem; position: absolute; animation: floatUp 4s ease-in-out infinite; user-select: none;
    }
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
    unsafe_allow_html=True,
)

# --- Load CSV ---
@st.cache_data
def load_data():
    df = pd.read_csv("spotify.csv")
    df.columns = df.columns.str.strip().str.lower()
    return df

df = load_data()

# --- App Title ---
st.title("🎧 Moodify — Your AI Music Companion")

# --- Floating Emojis ---
st.markdown(
    """
    <div class="floating-emojis">
        <span class="emoji emoji1">😊</span>
        <span class="emoji emoji2">😢</span>
        <span class="emoji emoji3">😎</span>
        <span class="emoji emoji4">⚡</span>
        <span class="emoji emoji5">💕</span>
        <span class="emoji emoji6">🕵‍♂</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- Mood keywords (AI-like filtering) ---
mood_keywords = {
    "Happy 😊": ["happy", "joy", "bright", "smile"],
    "Sad 😢": ["sad", "blue", "cry", "lonely"],
    "Chill 😎": ["chill", "relax", "slow", "lofi"],
    "Energetic ⚡": ["energy", "dance", "party", "power"],
    "Romantic 💕": ["love", "heart", "kiss", "romance"],
    "Mysterious 🕵‍♂": ["dark", "mystery", "shadow", "secret"],
}

mood = st.selectbox("Pick your mood:", list(mood_keywords.keys()) + ["Popular", "Long Songs", "Short Songs", "Random"])

# --- Filter logic ---
if mood in mood_keywords:
    keywords = mood_keywords[mood]
    filtered = df[df["track_name"].str.contains('|'.join(keywords), case=False, na=False)]
elif mood == "Popular":
    filtered = df[df["popularity"] > 85]
elif mood == "Long Songs":
    filtered = df[df["duration_min"] > 4]
elif mood == "Short Songs":
    filtered = df[df["duration_min"] < 3]
else:
    filtered = df.sample(5)

# --- Show recommended songs ---
st.markdown("### ✨ Your recommended songs:")
if not filtered.empty:
    sample = filtered.sample(min(5, len(filtered)))
    for _, row in sample.iterrows():
        st.write(f"🎵 {row['track_name']} by {row['artist']}")
else:
    st.warning("😕 No songs match this mood in your dataset.")

# --- Mystery Box ---
st.markdown("---")
st.header("🎁 Mystery Box — Open to get a surprise song!")

if 'mystery_opened' not in st.session_state:
    st.session_state.mystery_opened = False

if st.button("Open Mystery Box"):
    if not st.session_state.mystery_opened:
        st.session_state.mystery_opened = True
        with st.spinner("Opening your mystery box... 🎲"):
            time.sleep(3)
        mystery = df.sample(1).iloc[0]
        st.balloons()
        st.success(f"✨ You got: 🎶 {mystery['track_name']} by {mystery['artist']} ✨")
    else:
        st.info("You've already opened it! Refresh the page to try again.")

if st.button("🔄 Reset Mystery Box"):
    st.session_state.mystery_opened = False
    st.info("Mystery Box reset!")
    
    
 
      
   


    
      


   
   
  

   
       
    


