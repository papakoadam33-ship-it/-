import streamlit as st
import os

st.set_page_config(page_title="MARIOS PRO-BET PRO", page_icon="⚡", layout="centered")

# --- ΟΛΟΚΛΗΡΩΜΕΝΟ ΛΕΞΙΚΟ ΜΕΤΑΦΡΑΣΕΩΝ ΓΙΑ ΤΟ V3 ---
LEAGUE_TRANSLATIONS = {
    "Campeonato Brasileiro": "Πρωτάθλημα Βραζιλίας (Brasileirao) 🇧🇷",
    "Premier League": "Πρωτάθλημα Αγγλίας (Premier League) 🏴󠁧󠁢󠁧󠁥󠁮󠁧󠁿",
    "La Liga": "Πρωτάθλημα Ισπανίας (La Liga) 🇪🇸",
    "Serie A": "Πρωτάθλημα Ιταλίας (Serie A) 🇮🇹",
    "Bundesliga": "Πρωτάθλημα Γερμανίας (Bundesliga) 🇩🇪",
    "Ligue 1": "Πρωτάθλημα Γαλλίας (Ligue 1) 🇫🇷",
    "Champions League": "Champions League 🏆"
}

# --- PREMIUM DARK CSS DESIGN V3 ---
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
    
    /* Αναβαθμισμένη Κάρτα Αγώνα */
    .match-card { background-color: #1A1A1A; border: 1px solid #333333; border-left: 5px solid #FFD700; border-radius: 12px; padding: 20px; margin-bottom: 20px; }
    .league-label { color: #FCD34D; font-size: 13px; font-weight: bold; text-transform: uppercase; margin-bottom: 5px; }
    .teams-label { color: #FFFFFF; font-size: 20px; font-weight: bold; margin-bottom: 5px; }
    .time-badge { color: #9CA3AF; font-size: 13px; margin-bottom: 15px; }
    
    /* Στοιχεία Προγνωστικών */
    .prediction-row { display: flex; gap: 10px; margin-bottom: 10px; flex-wrap: wrap; }
    .tip-main { background-color: #CCA43B; color: #000000; padding: 8px 15px; border-radius: 6px; font-weight: bold; font-size: 15px; flex: 1; min-width: 120px; text-align: center; }
    .odds-badge { background-color: #1F2937; color: #FCD34D; padding: 8px 15px; border-radius: 6px; font-weight: bold; font-size: 15px; border: 1px solid #374151; text-align: center; }
    .stake-badge { background-color: #065F46; color: #34D399; padding: 8px 15px; border-radius: 6px; font-weight: bold; font-size: 15px; text-align: center; }
    .scores-box { background-color: #111827; border: 1px solid #1F2937; padding: 10px; border-radius: 6px; font-size: 13px; color: #9CA3AF; margin-top: 5px; }
    .stars-label { color: #FBBF24; font-size: 14px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# Κεντρικός VIP Τίτλος
st.markdown("""
    <div class="header-box">
        <div class="header-title">⚡ MARIOS PRO-BET PRO ⚡</div>
        <div class="header-subtitle">Poisson Distribution & Kelly Criterion V3</div>
    </div>
""", unsafe_allow_html=True)

filename = "daily_predictions.txt"
match_found = False
timestamp = "Live"
matches_to_render = []

# 1. Ανάγνωση και σωστό Parsing των V3 δεδομένων
if os.path.exists(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readlines()
            
        if lines:
            # Διάβασμα της νέας επικεφαλίδας του V3
            first_line = lines[0].strip()
            if "--- ΥΒΡΙΔΙΚΑ ΠΡΟΓΝΩΣΤΙΚΑ V3" in first_line:
                timestamp = first_line.replace("--- ΥΒΡΙΔΙΚΑ ΠΡΟΓΝΩΣΤΙΚΑ V3 (", "").replace(") ---", "")
            
            for line in lines:
                if line.startswith("---") or line.startswith("ΛΙΓΚΑ") or not line.strip():
                    continue
                    
                parts = line.strip().split("|")
                # Ο V3 Scraper παράγει ακριβώς 8 στήλες διαχωρισμένες με |
                if len(parts) == 8:
                    matches_to_render.append(parts)
                    match_found = True
    except Exception as e:
        pass

# 2. Σχεδιασμός του Interface με τα νέα δεδομένα
st.markdown(f'<div class="date-badge">📅 ΕΝΗΜΕΡΩΣΗ: {timestamp}</div>', unsafe_allow_html=True)
st.markdown('<div class="vip-section-title">🔥 VIP PICKS & KELLY STAKES</div>', unsafe_allow_html=True)

if match_found:
    for parts in matches_to_render:
        league_raw = parts[0]
        teams = parts[1]
        match_time = parts[2]
        tip_with_pct = parts[3]
        stars = parts[4]
        odds_str = parts[5]
        stake_str = parts[6]
        scores_str = parts[7]
        
        # Μετάφραση Λίγκας
        greek_league = LEAGUE_TRANSLATIONS.get(league_raw, league_raw)
        
        # Δημιουργία της V3 Κάρτας Αγώνα
        st.markdown(f"""
            <div class="match-card">
                <div class="league-label">🏆 {greek_league}</div>
                <div class="teams-label">{teams}</div>
                <div class="time-badge">🕒 {match_time} &nbsp;|&nbsp; <span class="stars-label">{stars}</span></div>
                <div class="prediction-row">
                    <div class="tip-main">👑 {tip_with_pct}</div>
                    <div class="odds-badge">📊 {odds_str}</div>
                    <div class="stake-badge">💰 {stake_str}</div>
                </div>
                <div class="scores-box">
                    🎯 <b>Πιθανά Σκόρ (Poisson):</b> {scores_str}
                </div>
            </div>
        """, unsafe_allow_html=True)
else:
    st.info("ℹ️ Δεν υπάρχουν διαθέσιμα προγνωστικά αυτή τη στιγμή. Βεβαιώσου ότι έχει τρέξει επιτυχώς ο Scraper (main.py).")

