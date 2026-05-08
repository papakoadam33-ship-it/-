import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Marios Pro-Bet", page_icon="⚽", layout="wide")

# Custom CSS για να μοιάζει με mobile app και να έχει ωραίες κάρτες
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; }
    .prediction-card {
        background-color: #1e2130;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #4CAF50;
        margin-bottom: 15px;
        transition: transform 0.3s;
    }
    .prediction-card:hover { transform: scale(1.01); }
    .league-label { color: #3b82f6; font-size: 0.8rem; font-weight: bold; text-transform: uppercase; }
    .match-title { font-size: 1.2rem; font-weight: bold; margin: 10px 0; color: white; }
    .tip-box {
        background-color: #2e3440;
        padding: 8px 12px;
        border-radius: 8px;
        display: inline-block;
        color: #00ff88;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- API DATA FETCHING ---
@st.cache_data(ttl=3600) # Κρατάει τα δεδομένα για 1 ώρα για ταχύτητα
def fetch_data():
    url = "https://api.football-data.org/v4/matches"
    headers = { 'X-Auth-Token': 'a1a4edf072dc4b2c8153fced44c88de9' }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json().get('matches', [])
    except Exception as e:
        return []

def get_tip(league_name):
    l_up = league_name.upper()
    if "COPA LIBERTADORES" in l_up: return "Goal-Goal"
    elif "BUNDESLIGA" in l_up or "LIGUE 1" in l_up: return "Over 2.5"
    elif "PREMIER LEAGUE" in l_up: return "1 & Over 1.5"
    elif "SERIE A" in l_up or "CHAMPIONSHIP" in l_up: return "2-3 Goals"
    return "1X & Over 1.5"

# --- SIDEBAR (ΦΙΛΤΡΑ) ---
st.sidebar.title("🔍 Φίλτρα & Αναζήτηση")
search_query = st.sidebar.text_input("Αναζήτηση ομάδας", "")

# --- MAIN UI ---
col1, col2 = st.columns([2, 1])
with col1:
    st.title("⚽ Marios Pro-Bet")
with col2:
    now = datetime.now()
    st.info(f"📅 {now.strftime('%d/%m/%Y')} | ⏰ {now.strftime('%H:%M')}")

matches = fetch_data()

if matches:
    # Λίστα για τα φίλτρα διοργάνωσης
    all_leagues = sorted(list(set([m['competition']['name'] for m in matches])))
    selected_league = st.sidebar.selectbox("Επιλογή Διοργάνωσης", ["Όλες"] + all_leagues)

    # Φιλτράρισμα δεδομένων
    filtered_matches = []
    for m in matches:
        league = m['competition']['name']
        home = m['homeTeam']['name']
        away = m['awayTeam']['name']
        
        # Έλεγχος φίλτρων
        if (selected_league == "Όλες" or selected_league == league) and \
           (search_query.lower() in home.lower() or search_query.lower() in away.lower()):
            filtered_matches.append(m)

    # Εμφάνιση Καρτών
    if filtered_matches:
        for m in filtered_matches[:40]:
            league = m['competition']['name']
            home = m['homeTeam']['name']
            away = m['awayTeam']['name']
            status = m.get('status')
            score = f"{m['score']['fullTime']['home']} - {m['score']['fullTime']['away']}" if status in ['IN_PLAY', 'FINISHED'] else ""
            
            tip = get_tip(league)
            
            # HTML Card
            live_tag = f"<span style='color:red;'>● LIVE: {score}</span>" if status == 'IN_PLAY' else ""
            
            st.markdown(f"""
                <div class="prediction-card">
                    <div class="league-label">🏆 {league}</div>
                    <div class="match-title">{home} vs {away} {live_tag}</div>
                    <div class="tip-box">🎯 Πρόβλεψη: {tip}</div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("Δεν βρέθηκαν αγώνες με αυτά τα κριτήρια.")
else:
    st.error("Αδυναμία σύνδεσης με το API. Ελέγξτε το κλειδί σας ή το όριο κλήσεων.")

# --- FOOTER ---
st.markdown("---")
st.caption("Marios Pro-Bet v2.0 | Data provided by football-data.org")
