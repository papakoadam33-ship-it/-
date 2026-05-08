import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# --- CONFIGURATION ΣΕΛΙΔΑΣ ---
st.set_page_config(page_title="Marios Pro-Bet", page_icon="⚽", layout="wide")

# --- CUSTOM CSS (STYLE) ---
st.markdown("""
    <style>
    /* Γενικό Background */
    .main { background-color: #0e1117; }
    
    /* Στυλ για την ημερομηνία στην κορυφή */
    .date-container {
        background-color: #1e2130;
        padding: 15px;
        border-radius: 12px;
        text-align: center;
        color: #3b82f6;
        font-weight: bold;
        font-size: 1.1rem;
        margin-bottom: 25px;
        border: 1px solid #2d324a;
    }

    /* Live Pulse Effect (Αναβοσβήνει) */
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.4; }
        100% { opacity: 1; }
    }
    .live-tag {
        color: #ff4b4b;
        font-weight: bold;
        animation: pulse 1.5s infinite;
        font-size: 0.9rem;
    }

    /* Στυλ Κάρτας Αγώνα */
    .prediction-card {
        background-color: #1e2130;
        padding: 25px;
        border-radius: 15px;
        border-left: 6px solid #4CAF50;
        margin-bottom: 18px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        transition: transform 0.2s;
    }
    .prediction-card:hover {
        transform: translateY(-3px);
        border-left-color: #00ff88;
    }

    .league-label {
        color: #8892b0;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }

    .match-title {
        font-size: 1.3rem;
        font-weight: bold;
        color: #ffffff;
        margin: 5px 0 15px 0;
    }

    .tip-container {
        background-color: #25293d;
        padding: 10px 15px;
        border-radius: 8px;
        display: inline-flex;
        align-items: center;
        border: 1px solid #3b4261;
    }

    .tip-icon { margin-right: 8px; }
    .tip-text { color: #00ff88; font-weight: bold; font-size: 1rem; }
    </style>
    """, unsafe_allow_html=True)

# --- ΣΥΝΑΡΤΗΣΕΙΣ ΔΕΔΟΜΕΝΩΝ ---
@st.cache_data(ttl=600) # Ανανέωση κάθε 10 λεπτά για live σκορ
def get_football_data():
    url = "https://api.football-data.org/v4/matches"
    headers = { 'X-Auth-Token': 'a1a4edf072dc4b2c8153fced44c88de9' }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get('matches', [])
    except:
        return []

def generate_tip(league_name):
    l_up = league_name.upper()
    if "COPA LIBERTADORES" in l_up: return "Goal-Goal"
    elif "BUNDESLIGA" in l_up or "LIGUE 1" in l_up: return "Over 2.5"
    elif "PREMIER LEAGUE" in l_up: return "1 & Over 1.5"
    elif "SERIE A" in l_up or "CHAMPIONSHIP" in l_up: return "2-3 Goals"
    return "1X & Over 1.5"

# --- SIDEBAR ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/53/53283.png", width=80)
st.sidebar.title("Marios Pro-Bet Control")
st.sidebar.markdown("---")
search = st.sidebar.text_input("🔍 Αναζήτηση Ομάδας", "")

# --- MAIN APP ---
st.title("⚽ Marios Pro-Bet")

# Ημερομηνία και ώρα
now = datetime.now()
st.markdown(f"""
    <div class="date-container">
        📅 {now.strftime('%d/%m/%Y')} &nbsp;&nbsp; | &nbsp;&nbsp; ⏰ {now.strftime('%H:%M')}
    </div>
    """, unsafe_allow_html=True)

matches = get_football_data()

if matches:
    # Δημιουργία λίστας για φίλτρο διοργανώσεων
    leagues = sorted(list(set([m['competition']['name'] for m in matches])))
    selected_league = st.sidebar.selectbox("🏆 Επιλογή Διοργάνωσης", ["Όλες οι Λίγκες"] + leagues)

    # Φιλτράρισμα
    display_count = 0
    for m in matches:
        league = m['competition']['name']
        home = m['homeTeam']['name']
        away = m['awayTeam']['name']
        status = m['status']
        
        # Λογική φίλτρων
        if (selected_league == "Όλες οι Λίγκες" or selected_league == league) and \
           (search.lower() in home.lower() or search.lower() in away.lower()):
            
            display_count += 1
            tip = generate_tip(league)
            
            # Διαχείριση Live Σκορ
            score_html = ""
            if status == "IN_PLAY":
                h_score = m['score']['fullTime']['home']
                a_score = m['score']['fullTime']['away']
                score_html = f"<span class='live-tag'> ● LIVE: {h_score} - {a_score}</span>"
            elif status == "FINISHED":
                h_score = m['score']['fullTime']['home']
                a_score = m['score']['fullTime']['away']
                score_html = f"<span style='color:#8892b0; font-size:0.9rem;'> (Τελικό: {h_score}-{a_score})</span>"

            # Εμφάνιση Κάρτας
            st.markdown(f"""
                <div class="prediction-card">
                    <div class="league-label">🏆 {league}</div>
                    <div class="match-title">{home} vs {away} {score_html}</div>
                    <div class="tip-container">
                        <span class="tip-icon">🎯</span>
                        <span class="tip-text">Πρόβλεψη: {tip}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            if display_count >= 40: break

    if display_count == 0:
        st.warning("Δεν βρέθηκαν αγώνες για τα κριτήρια που θέσατε.")
else:
    st.error("⚠️ Πρόβλημα στη λήψη δεδομένων. Δοκιμάστε ξανά σε λίγο.")

st.markdown("---")
st.caption("© 2026 Marios Pro-Bet | Powered by Football-Data.org API")
