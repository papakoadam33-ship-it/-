import streamlit as st
import requests
from datetime import datetime, timedelta

# --- ΡΥΘΜΙΣΗ ΣΕΛΙΔΑΣ ---
st.set_page_config(page_title="Marios Pro-Bet Pro", layout="centered")

# --- ΡΥΘΜΙΣΕΙΣ API ---
RAPID_API_KEY = "47d5da2fb8mshde110deccc94426p115d5ajsnd9cc939fa561"
HEADERS = {"X-RapidAPI-Key": RAPID_API_KEY}

@st.cache_data(ttl=3600)  # Cache για 1 ώρα για να μην "καεί" το API Key
def fetch_all_predictions():
    all_preds = []
    today = datetime.now().strftime('%Y-%m-%d')
    
    # --- ΠΗΓΗ 1: ApiFootball ---
    try:
        url1 = "https://apifootball3.p.rapidapi.com/"
        params1 = {"action": "get_predictions", "from": today, "to": today}
        r1 = requests.get(url1, headers=HEADERS, params=params1, timeout=10)
        data1 = r1.json()
        if isinstance(data1, list):
            for item in data1:
                all_preds.append({
                    "league": f"🏆 {item.get('league_name', 'FOOTBALL')}",
                    "teams": f"{item.get('match_hometeam_name')} - {item.get('match_awayteam_name')}",
                    "tip": "Over 2.5", "prob": f"{item.get('prob_O', '75')}%",
                    "cover": "GG", "cover_prob": f"{item.get('prob_bts', '65')}%"
                })
    except: pass

    # --- ΠΗΓΗ 2: Football Prediction ---
    try:
        url2 = "https://football-prediction-api.p.rapidapi.com/api/v2/predictions"
        r2 = requests.get(url2, headers=HEADERS, params={"iso_date": today}, timeout=10)
        data2 = r2.json()
        if "data" in data2:
            for item in data2["data"]:
                pred = item.get('prediction', '1X')
                prob = item.get('probabilities', {}).get(pred, "80")
                all_preds.append({
                    "league": f"⚽ {item.get('federation', 'INTL')}",
                    "teams": f"{item.get('home_team')} - {item.get('away_team')}",
                    "tip": pred, "prob": f"{prob}%",
                    "cover": "Over 1.5", "cover_prob": "85%"
                })
    except: pass
    
    return all_preds

# --- UI ΕΜΦΑΝΙΣΗ ---
st.markdown("<h1 style='text-align: center;'>⚡ MARIOS PRO-BET PRO ⚡</h1>", unsafe_allow_html=True)
st.sidebar.header("Settings")
if st.sidebar.button("🔄 Refresh Data"):
    st.cache_data.clear()

preds = fetch_all_predictions()

if not preds:
    st.warning("⚠️ Αναμονή για δεδομένα από τα API. Δοκίμασε ξανά σε λίγο.")
else:
    # Αφαίρεση διπλοτύπων
    unique_matches = {}
    for p in preds:
        if p['teams'] not in unique_matches:
            unique_matches[p['teams']] = p

    for m in unique_matches.values():
        st.markdown(f"""
        <div style="background-color: #1e2130; padding: 20px; border-radius: 15px; margin-bottom: 20px; border-left: 5px solid #f1c40f; color: white;">
            <p style="color: #f1c40f; font-weight: bold; margin-bottom: 5px;">{m['league']}</p>
            <h3 style="margin: 0; color: white;">{m['teams']}</h3>
            <hr style="border: 0.5px solid #34495e;">
            <div style="display: flex; justify-content: space-between;">
                <div style="color: #e74c3c; font-weight: bold;">🎯 {m['tip']} ({m['prob']})</div>
                <div style="color: #95a5a6;">🛡️ {m['cover']} ({m['cover_prob']})</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

