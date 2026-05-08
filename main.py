import streamlit as st
import requests
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Marios Pro-Bet AI", page_icon="🤖", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .prediction-card {
        background-color: #1e2130;
        padding: 20px;
        border-radius: 15px;
        border-left: 6px solid #3b82f6;
        margin-bottom: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    .league-label { color: #8892b0; font-size: 0.8rem; font-weight: bold; }
    .match-title { font-size: 1.2rem; font-weight: bold; color: white; margin: 5px 0; }
    .tip-box {
        background-color: #25293d;
        padding: 8px 12px;
        border-radius: 8px;
        color: #00ff88;
        font-weight: bold;
        display: inline-block;
        border: 1px solid #3b4261;
    }
    .confidence-bar {
        height: 8px;
        background-color: #2d324a;
        border-radius: 5px;
        margin-top: 10px;
        overflow: hidden;
    }
    .confidence-fill {
        height: 100%;
        background: linear-gradient(90deg, #3b82f6, #00ff88);
    }
    .live-dot {
        color: #ff4b4b;
        animation: blink 1s infinite;
        font-weight: bold;
    }
    @keyframes blink { 0% {opacity: 1;} 50% {opacity: 0.3;} 100% {opacity: 1;} }
    </style>
    """, unsafe_allow_html=True)

# --- AI LOGIC (THE "INTELLIGENCE") ---
def calculate_ai_prediction(match):
    """
    Αυτή η συνάρτηση προσομοιώνει την 'ευφυΐα' αναλύοντας 
    τα δεδομένα του αγώνα και της διοργάνωσης.
    """
    league = match['competition']['name'].upper()
    home_team = match['homeTeam']['name']
    
    # Βασική πιθανότητα
    confidence = 65 
    
    # 1. Έξυπνη επιλογή σημείου βάσει ιστορικών δεδομένων λιγκών
    if any(x in league for x in ["BUNDESLIGA", "NETHERLANDS", "NORWAY"]):
        tip = "Over 2.5 Goals"
        confidence += 12
    elif any(x in league for x in ["SERIE A", "GREECE", "ARGENTINA"]):
        tip = "Under 3.5 Goals"
        confidence += 8
    elif "PREMIER LEAGUE" in league:
        tip = "Goal-Goal"
        confidence += 15
    else:
        tip = "1X & Over 1.5"
        confidence += 5

    # 2. Ανάλυση αν ο αγώνας είναι LIVE (Δυναμική Ευφυΐα)
    if match['status'] == "IN_PLAY":
        h_score = match['score']['fullTime']['home']
        a_score = match['score']['fullTime']['away']
        # Αν είναι στο 0-0 μετά από ώρα, αυξάνουμε την πιθανότητα για Late Goal
        if h_score + a_score == 0:
            tip = "Next Goal: Home or Away"
            confidence += 10
        else:
            confidence += 5

    # Περιορισμός στο 98%
    confidence = min(confidence, 98)
    
    return tip, confidence

# --- DATA FETCHING ---
@st.cache_data(ttl=300) # Ανανέωση κάθε 5 λεπτά
def get_data():
    url = "https://api.football-data.org/v4/matches"
    headers = { 'X-Auth-Token': 'a1a4edf072dc4b2c8153fced44c88de9' }
    try:
        r = requests.get(url, headers=headers)
        return r.json().get('matches', [])
    except:
        return []

# --- UI ---
st.title("⚽ Marios Pro-Bet AI")
st.sidebar.header("AI Settings")
st.sidebar.write("Ο αλγόριθμος αναλύει δεδομένα λιγκών και live ροής.")

data = get_data()

if data:
    # Φίλτρο αναζήτησης
    search = st.sidebar.text_input("Αναζήτηση Ομάδας", "")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        st.write(f"⏰ {datetime.now().strftime('%H:%M:%S')}")

    for m in data[:40]:
        home = m['homeTeam']['name']
        away = m['awayTeam']['name']
        league = m['competition']['name']
        status = m['status']
        
        if search.lower() in home.lower() or search.lower() in away.lower():
            # Εκτέλεση AI ανάλυσης
            tip, conf = calculate_ai_prediction(m)
            
            # Score display
            score_text = ""
            if status == "IN_PLAY":
                score_text = f"<span class='live-dot'> ● LIVE {m['score']['fullTime']['home']}-{m['score']['fullTime']['away']}</span>"
            
            # Σχεδίαση Κάρτας
            st.markdown(f"""
                <div class="prediction-card">
                    <div class="league-label">🏆 {league}</div>
                    <div class="match-title">{home} vs {away} {score_text}</div>
                    <div class="tip-box">🎯 AI Tip: {tip}</div>
                    <div style="margin-top:10px; font-size:0.8rem; color:#8892b0;">
                        Πιθανότητα Επιτυχίας: {conf}%
                    </div>
                    <div class="confidence-bar">
                        <div class="confidence-fill" style="width: {conf}%;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
else:
    st.error("Δεν βρέθηκαν δεδομένα. Ελέγξτε το API Key.")

