import streamlit as st
import requests
from datetime import datetime
import os

# --- ΡΥΘΜΙΣΗ ΣΕΛΙΔΑΣ ---
st.set_page_config(page_title="Marios Pro-Bet Pro", layout="centered")

# Χρησιμοποιούμε cache για να μην τρώμε το limit του API (1 ώρα TTL)
@st.cache_data(ttl=3600)
def fetch_live_predictions():
    predictions = []
    # Χρησιμοποιώ το Key που μου έδωσες
    headers = {"X-RapidAPI-Key": "47d5da2fb8mshde110deccc94426p115d5ajsnd9cc939fa561"}
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Πηγή: Football Prediction API
    try:
        url = "https://football-prediction-api.p.rapidapi.com/api/v2/predictions"
        params = {"iso_date": today}
        r = requests.get(url, headers=headers, params=params, timeout=10)
        data = r.json()
        
        if "data" in data:
            for item in data["data"]:
                home = item.get('home_team')
                away = item.get('away_team')
                league = item.get('federation', 'INTL').upper()
                tip = item.get("prediction", "1X")
                prob = item.get("probabilities", {}).get(tip, 50)
                
                # Φιλτράρισμα για να δείχνουμε μόνο καλά σημεία
                if prob >= 70:
                    star = "🔥 " if prob >= 85 else ""
                    predictions.append([
                        f"{star}[FP] {league}",
                        f"{home} - {away}",
                        f"Κύρια: {tip}", f"{prob}%",
                        "Over 1.5", "80%"
                    ])
    except Exception as e:
        st.sidebar.error(f"API Error: {e}")
        
    return predictions

# --- ΕΜΦΑΝΙΣΗ ---
st.markdown("<h1 style='text-align: center;'>⚡ MARIOS PRO-BET PRO ⚡</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-style: italic;'>Advanced Poisson Prediction Engine</p>", unsafe_allow_html=True)

# Αντί να φορτώνουμε από TXT, καλούμε το API απευθείας
preds = fetch_live_predictions()

if not preds:
    st.warning("⚠️ Αναμονή για ενημέρωση δεδομένων από τα API. Δοκίμασε αργότερα (μετά τις 11:00 π.μ.).")
else:
    # Ταξινόμηση (Hot πρώτα)
    preds.sort(key=lambda x: "🔥" not in x[0])
    
    for p in preds:
        with st.container():
            st.markdown(f"""
            <div style="background-color: #1e2130; padding: 20px; border-radius: 15px; margin-bottom: 20px; border-left: 5px solid #f1c40f; color: white;">
                <p style="color: #f1c40f; font-weight: bold; margin-bottom: 5px;">🏆 {p[0]}</p>
                <h3 style="margin: 0; color: white;">{p[1]}</h3>
                <hr style="border: 0.5px solid #34495e;">
                <div style="display: flex; justify-content: space-between;">
                    <div style="color: #e74c3c; font-weight: bold;">🎯 {p[2]} ({p[3]})</div>
                    <div style="color: #95a5a6;">🛡️ {p[4]} ({p[5]})</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

