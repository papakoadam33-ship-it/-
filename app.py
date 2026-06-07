import streamlit as st
import os

st.set_page_config(page_title="MARIOS PRO-BET", page_icon="⚡", layout="centered")

# --- ΛΕΞΙΚΟ ΜΕΤΑΦΡΑΣΕΩΝ ---
LEAGUE_TRANSLATIONS = {
    "Premier League": "Πρωτάθλημα Αγγλίας (Premier League) 🏴󠁧󠁢󠁥󠁮󠁧󠁿",
    "La Liga": "Πρωτάθλημα Ισπανίας (La Liga) 🇪🇸",
    "Serie A": "Πρωτάθλημα Ιταλίας (Serie A) 🇮🇹",
    "Bundesliga": "Πρωτάθλημα Γερμανίας (Bundesliga) 🇩🇪",
    "Ligue 1": "Πρωτάθλημα Γαλλίας (Ligue 1) 🇫🇷",
    "Champions League": "Champions League 🏆",
    "Euro": "Euro 🇪🇺",
    "World Cup": "World Cup 🌎"
}

# --- PREMIUM DARK CSS DESIGN ---
st.markdown("""
    <style>
    .stApp { background-color: #121212; color: #FFFFFF; }
    .header-box {
        background-color: #1E1E1E; padding: 25px; border-radius: 15px;
        text-align: center; border: 2px solid #FFD700; margin-bottom: 20px;
        box-shadow: 0px 4px 15px rgba(255, 215, 0, 0.2);
    }
    .header-title { font-size: 28px; font-weight: 900; color: #FFFFFF; letter-spacing: 1px; margin: 0; }
    .header-subtitle { font-size: 16px; font-style: italic; color: #FFD700; margin-top: 10px; }
    .date-badge {
        background-color: #1E1E1E; color: #FFD700; padding: 10px; border-radius: 8px;
        text-align: center; font-weight: bold; font-size: 15px; border: 1px solid #FFD700; margin-bottom: 25px;
    }
    .vip-section-title { color: #F87171; font-size: 22px; font-weight: bold; margin-top: 20px; margin-bottom: 15px; }
    
    /* Κάρτα Αγώνα */
    .match-card { background-color: #1A1A1A; border: 1px solid #333333; border-left: 5px solid #FFD700; border-radius: 12px; padding: 20px; margin-bottom: 20px; }
    .league-label { color: #FCD34D; font-size: 13px; font-weight: bold; text-transform: uppercase; margin-bottom: 5px; }
    .teams-label { color: #FFFFFF; font-size: 20px; font-weight: bold; margin-bottom: 5px; }
    .time-badge { color: #9CA3AF; font-size: 13px; margin-bottom: 15px; }
    
    /* Σειρά Προγνωστικών */
    .prediction-row { display: flex; gap: 10px; margin-bottom: 10px; flex-wrap: wrap; }
    .tip-main { background-color: #CCA43B; color: #000000; padding: 8px 15px; border-radius: 6px; font-weight: bold; font-size: 15px; flex: 1; min-width: 120px; text-align: center; }
    .pct-badge { background-color: #1F2937; color: #FCD34D; padding: 8px 15px; border-radius: 6px; font-weight: bold; font-size: 15px; border: 1px solid #374151; text-align: center; }
    .cover-badge { background-color: #111827; color: #9CA3AF; padding: 8px 15px; border-radius: 6px; font-size: 15px; border: 1px solid #1F2937; text-align: center; flex: 1; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="header-box">
        <div class="header-title">⚡ MARIOS PRO-BET PRO ⚡</div>
        <div class="header-subtitle">Poisson Distribution Model</div>
    </div>
""", unsafe_allow_html=True)

filename = "daily_predictions.txt"
match_found = False
timestamp = "Live"
matches_to_render = []

if os.path.exists(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readlines()
        if lines:
            first_line = lines[0].strip()
            if "--- ΠΡΟΓΝΩΣΤΙΚΑ" in first_line:
                timestamp = first_line.replace("--- ΠΡΟΓΝΩΣΤΙΚΑ ", "").replace(" ---", "")
            
            for line in lines:
                clean_line = line.strip()
                if clean_line.startswith("---") or clean_line.startswith("ΛΙΓΚΑ") or not clean_line:
                    continue
                parts = clean_line.split("|")
                # Έλεγχος για τις 6 στήλες του αρχικού σου κώδικα
                if len(parts) >= 5:
                    matches_to_render.append(parts)
                    match_found = True
    except Exception:
        timestamp = "Live"

st.markdown(f'<div class="date-badge">📅 ΕΝΗΜΕΡΩΣΗ: {timestamp}</div>', unsafe_allow_html=True)
st.markdown('<div class="vip-section-title">🔥 VIP PICKS (ΥΨΗΛΟ ΠΟΣΟΣΤΟ)</div>', unsafe_allow_html=True)

if match_found:
    for parts in matches_to_render:
        league_raw = parts[0]
        teams = parts[1]
        match_time = parts[2]
        tip = parts[3]
        pct = parts[4]
        cover = parts[5] if len(parts) > 5 else "-"
        
        st.markdown(f"""
            <div class="match-card">
                <div class="league-label">🏆 {LEAGUE_TRANSLATIONS.get(league_raw, league_raw)}</div>
                <div class="teams-label">{teams}</div>
                <div class="time-badge">🕒 Ώρα: {match_time}</div>
                <div class="prediction-row">
                    <div class="tip-main">👑 {tip}</div>
                    <div class="pct-badge">🎯 {pct}%</div>
                    <div class="cover-badge">🛡️ Κάλυψη: {cover}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
else:
    st.info("ℹ️ Δεν υπάρχουν προγνωστικά διαθέσιμα για σήμερα στις επιλεγμένες λίγκες.")
