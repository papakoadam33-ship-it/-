import streamlit as st
import requests
from datetime import datetime, timedelta

# --- 1. ΡΥΘΜΙΣΗ ΣΕΛΙΔΑΣ ---
st.set_page_config(page_title="Marios Pro-Bet Pro", layout="centered")

# --- 2. CUSTOM CSS (DARK THEME) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .prediction-card {
        background-color: #1e2130; 
        padding: 20px; 
        border-radius: 15px; 
        margin-bottom: 20px; 
        border-left: 5px solid #f1c40f; 
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ΛΟΓΙΚΗ ΑΝΑΚΤΗΣΗΣ ΔΕΔΟΜΕΝΩΝ ---
@st.cache_data(ttl=3600)
def get_all_data():
    api_key = "47d5da2fb8mshde110deccc94426p115d5ajsnd9cc939fa561"
    headers = {"X-RapidAPI-Key": api_key, "X-RapidAPI-Host": "football-prediction-api.p.rapidapi.com"}
    
    # Δοκιμή για σήμερα και αύριο
    for i in range(2):
        date_str = (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d')
        try:
            url = "https://football-prediction-api.p.rapidapi.com/api/v2/predictions"
            r = requests.get(url, headers=headers, params={"iso_date": date_str}, timeout=10)
            data = r.json().get("data", [])
            if data: return data, date_str
        except: continue
    
    return [], None

# --- 4. ΕΜΦΑΝΙΣΗ UI ---
st.markdown("<h1 style='text-align: center; color: #f1c40f;'>⚡ MARIOS PRO-BET PRO ⚡</h1>", unsafe_allow_html=True)

preds, active_date = get_all_data()

if not preds:
    st.sidebar.error("API Limit reached / No games found")
    # BACKUP DATA ΓΙΑ ΝΑ ΜΗΝ ΕΙΝΑΙ ΑΔΕΙΟ ΤΟ SITE ΣΟΥ
    preds = [
        {"home_team": "Παράδειγμα Ομάδας Α", "away_team": "Παράδειγμα Ομάδας Β", "federation": "DEMO", "prediction": "1", "probabilities": {"1": 88}}
    ]
    active_date = "Demo Mode"

st.sidebar.info(f"📅 Ημερομηνία: {active_date}")

for item in preds:
    home = item.get('home_team')
    away = item.get('away_team')
    league = item.get('federation', 'INTL').upper()
    tip = item.get('prediction', '1X')
    prob = item.get('probabilities', {}).get(tip, 75)
    
    st.markdown(f"""
    <div class="prediction-card">
        <p style="color: #f1c40f; font-weight: bold; margin-bottom: 5px;">🏆 {league}</p>
        <h3 style="margin: 0; color: white;">{home} - {away}</h3>
        <hr style="border: 0.5px solid #34495e;">
        <div style="display: flex; justify-content: space-between;">
            <div style="color: #e74c3c; font-weight: bold;">🎯 Πρόβλεψη: {tip} ({prob}%)</div>
            <div style="color: #95a5a6;">🛡️ Κάλυψη: Over 1.5</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

if st.sidebar.button("🔄 Force Refresh"):
    st.cache_data.clear()
    st.rerun()
