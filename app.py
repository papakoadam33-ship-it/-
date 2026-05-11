import streamlit as st
import requests
from datetime import datetime, timedelta

# --- 1. ΡΥΘΜΙΣΗ ΣΕΛΙΔΑΣ ---
st.set_page_config(page_title="Marios Pro-Bet Pro", layout="centered")

# --- 2. CUSTOM CSS (DARK THEME & STYLING) ---
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
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background-color: #f1c40f;
        color: black;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ΛΟΓΙΚΗ ΑΝΑΚΤΗΣΗΣ ΔΕΔΟΜΕΝΩΝ ΜΕ CACHE 4 ΩΡΩΝ ---
@st.cache_data(ttl=14400) # <--- ΕΔΩ ΕΙΝΑΙ ΤΟ "ΦΡΕΝΟ" ΓΙΑ ΤΟ API LIMIT (4 ΩΡΕΣ)
def get_all_data():
    api_key = "47d5da2fb8mshde110deccc94426p115d5ajsnd9cc939fa561"
    headers = {
        "X-RapidAPI-Key": api_key, 
        "X-RapidAPI-Host": "football-prediction-api.p.rapidapi.com"
    }
    
    # Δοκιμάζει σήμερα (offset=0) και αύριο (offset=1)
    for i in range(2):
        date_str = (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d')
        try:
            url = "https://football-prediction-api.p.rapidapi.com/api/v2/predictions"
            r = requests.get(url, headers=headers, params={"iso_date": date_str}, timeout=10)
            
            if r.status_code == 200:
                data = r.json().get("data", [])
                if data: 
                    return data, date_str, "OK"
            elif r.status_code == 429:
                return [], None, "LIMIT"
        except:
            continue
    
    return [], None, "EMPTY"

# --- 4. ΕΜΦΑΝΙΣΗ UI ---
st.markdown("<h1 style='text-align: center; color: #f1c40f;'>⚡ MARIOS PRO-BET PRO ⚡</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>Advanced Poisson Prediction Engine</p>", unsafe_allow_html=True)

preds, active_date, status = get_all_data()

# Sidebar πληροφορίες
st.sidebar.header("📊 Control Panel")

if status == "LIMIT":
    st.sidebar.error("🚫 API Limit reached για σήμερα.")
    st.warning("⚠️ Τα δωρεάν όρια του API εξαντλήθηκαν. Εμφάνιση Demo Προγνωστικών.")
    # Demo δεδομένα για να μην είναι άδεια η σελίδα
    preds = [{"home_team": "Tottenham", "away_team": "Benfica", "federation": "UEFA", "prediction": "Over 2.5", "probabilities": {"Over 2.5": 82}}]
    active_date = "Demo Mode"
elif status == "EMPTY":
    st.sidebar.warning("⏳ Δεν βρέθηκαν αγώνες.")
    st.info("ℹ️ Αναμονή για ενημέρωση δεδομένων. Δοκιμάστε αργότερα.")
else:
    st.sidebar.success(f"✅ Δεδομένα ενεργά: {active_date}")

# Εμφάνιση προγνωστικών
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
        <hr style="border: 0.5px solid #34495e; margin: 15px 0;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="color: #e74c3c; font-weight: bold; font-size: 1.1rem;">
                🎯 Πρόβλεψη: {tip} <span style="color: white; font-size: 0.9rem;">({prob}%)</span>
            </div>
            <div style="color: #95a5a6; font-size: 0.9rem;">
                🛡️ Κάλυψη: Over 1.5
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Κουμπί Ανανέωσης στο Sidebar
if st.sidebar.button("🔄 Force Refresh"):
    st.cache_data.clear()
    st.rerun()
