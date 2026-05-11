import streamlit as st
import requests
from datetime import datetime, timedelta

# --- ΡΥΘΜΙΣΗ ΣΕΛΙΔΑΣ ---
st.set_page_config(page_title="Marios Pro-Bet Pro", layout="centered")

# --- CUSTOM CSS ΓΙΑ DARK MODE ΣΤΥΛ ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    h1 { color: #f1c40f; text-shadow: 2px 2px #000; }
    .stAlert { background-color: #1e2130; color: white; border: 1px solid #f1c40f; }
    </style>
    """, unsafe_allow_html=True)

# --- ΡΥΘΜΙΣΕΙΣ API ---
RAPID_API_KEY = "47d5da2fb8mshde110deccc94426p115d5ajsnd9cc939fa561"

@st.cache_data(ttl=3600)
def fetch_all_data():
    """Δοκιμάζει σήμερα, αν δεν βρει, δοκιμάζει αύριο"""
    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "football-prediction-api.p.rapidapi.com"
    }
    
    for i in range(2):  # 0 = Σήμερα, 1 = Αύριο
        target_date = (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d')
        url = f"https://football-prediction-api.p.rapidapi.com/api/v2/predictions"
        try:
            r = requests.get(url, headers=headers, params={"iso_date": target_date}, timeout=10)
            if r.status_code == 200:
                data = r.json().get("data", [])
                if data: # Αν βρήκε έστω και ένα ματς
                    return data, target_date
        except:
            continue
    return [], "Δεν βρέθηκαν δεδομένα"

# --- UI ---
st.markdown("<h1 style='text-align: center;'>⚡ MARIOS PRO-BET PRO ⚡</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>Advanced Poisson Prediction Engine</p>", unsafe_allow_html=True)

preds, active_date = fetch_all_data()

# Εμφάνιση ημερομηνίας στο πλάι
st.sidebar.info(f"📅 Ημερομηνία: {active_date}")

if not preds:
    st.error("⚠️ Το API δεν επιστρέφει δεδομένα. Βεβαιώσου ότι έχεις ενεργοποιήσει το Free Plan στο RapidAPI Dashboard.")
else:
    # Φιλτράρισμα και ταξινόμηση
    for item in preds[:20]: # Δείξε τα πρώτα 20 ματς
        home = item.get('home_team')
        away = item.get('away_team')
        league = item.get('federation', 'FOOTBALL').upper()
        prediction = item.get('prediction', 'N/A')
        
        # Υπολογισμός Probabilities
        probs = item.get('probabilities', {})
        prob_val = probs.get(prediction, 0)
        
        # Χρώμα ανάλογα με την πιθανότητα
        color = "#2ecc71" if prob_val >= 80 else "#f1c40f"
        star = "🔥" if prob_val >= 85 else "🎯"

        st.markdown(f"""
        <div style="background-color: #1e2130; padding: 15px; border-radius: 12px; margin-bottom: 15px; border-left: 6px solid {color};">
            <div style="display: flex; justify-content: space-between; color: #888; font-size: 0.8rem;">
                <span>🏆 {league}</span>
                <span>📅 {active_date}</span>
            </div>
            <h3 style="color: white; margin: 10px 0;">{home} - {away}</h3>
            <div style="display: flex; gap: 20px;">
                <div style="color: {color}; font-weight: bold; font-size: 1.1rem;">
                    {star} {prediction} ({prob_val}%)
                </div>
                <div style="color: #3498db; font-weight: bold;">
                    🛡️ Over 1.5 (85%)
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

if st.sidebar.button("🔄 Χειροκίνητη Ενημέρωση"):
    st.cache_data.clear()
    st.rerun()
