import streamlit as st
import os

st.set_page_config(page_title="MARIOS PRO-BET PRO", page_icon="⚡", layout="centered")

LEAGUE_TRANSLATIONS = {
    "Premier League": "Πρωτάθλημα Αγγλίας (Premier League)",
    "La Liga": "Πρωτάθλημα Ισπανίας (La Liga)",
    "Serie A": "Πρωτάθλημα Ιταλίας (Serie A)",
    "Bundesliga": "Πρωτάθλημα Γερμανίας (Bundesliga)",
    "Ligue 1": "Πρωτάθλημα Γαλλίας (Ligue 1)"
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
    .match-card { background-color: #1A1A10; border: 2px solid #FFD700; border-radius: 15px; padding: 20px; margin-bottom: 20px; }
    .league-label { color: #FCD34D; font-size: 14px; font-weight: bold; text-transform: uppercase; margin-bottom: 8px; }
    .teams-label { color: #FFFFFF; font-size: 22px; font-weight: bold; margin-bottom: 12px; }
    .time-badge { background-color: #EF4444; color: #FFFFFF; padding: 4px 10px; border-radius: 6px; font-size: 13px; font-weight: bold; display: inline-block; margin-bottom: 15px; }
    .tip-main { background-color: #CCA43B; color: #000000; padding: 12px; border-radius: 10px; text-align: center; font-weight: bold; font-size: 18px; margin-bottom: 10px; }
    .tip-cover { background-color: #D97706; color: #FFFFFF; padding: 12px; border-radius: 10px; text-align: center; font-weight: bold; font-size: 17px; }
    </style>
""", unsafe_allow_html=True)

# Κεντρικός VIP Τίτλος
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

# 1. Πρώτα διαβάζουμε και αναλύουμε τα δεδομένα
if os.path.exists(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readlines()
            
        if lines:
            # Ασφαλές διάβασμα της ημερομηνίας από την 1η γραμμή
            first_line = lines[0].strip()
            if "--- ΠΡΟΓΝΩΣΤΙΚΑ " in first_line:
                timestamp = first_line.replace("--- ΠΡΟΓΝΩΣΤΙΚΑ ", "").replace(" ---", "")
            
            # Φιλτράρισμα των αγώνων
            for line in lines:
                if line.startswith("---") or line.startswith("ΛΙΓΚΑ") or not line.strip():
                    continue
                    
                parts = line.strip().split("|")
                if len(parts) >= 5:
                    league_raw = parts[0]
                    if league_raw == "INFO":
                        continue
                    
                    matches_to_render.append(parts)
                    match_found = True
    except Exception as e:
        pass

# 2. Τώρα σχεδιάζουμε το Interface ΜΙΑ ΦΟΡΑ με τα σωστά στοιχεία
st.markdown(f'<div class="date-badge">📅 ΠΡΟΓΝΩΣΤΙΚΑ {timestamp}</div>', unsafe_allow_html=True)
st.markdown('<div class="vip-section-title">🔥 VIP PICKS (ΥΨΗΛΟ ΠΟΣΟΣΤΟ)</div>', unsafe_allow_html=True)

if match_found:
    # Σχεδίαση των καρτών αν βρέθηκαν αγώνες
    for parts in matches_to_render:
        league_raw = parts[0]
        teams = parts[1]
        match_time = parts[2]
        tip = parts[3]
        pct = parts[4]
        cover = parts[5] if len(parts) > 5 else "-"
        
        greek_league = LEAGUE_TRANSLATIONS.get(league_raw, league_raw)
        
        st.markdown(f"""
            <div class="match-card">
                <div class="league-label">🏆 {greek_league} [VIP]</div>
                <div class="teams-label">{teams}</div>
                <div class="time-badge">🕒 {match_time}</div>
                <div class="tip-main">👑 {tip} ({pct}%)</div>
                <div class="tip-cover">🛡️ {cover}</div>
            </div>
        """, unsafe_allow_html=True)
else:
    # Καθαρό μήνυμα χωρίς διπλότυπα αν είναι καθημερινή και δεν έχει ματς
    st.info("ℹ️ Δεν υπάρχουν προγνωστικά διαθέσιμα για τις 5 μεγάλες λίγκες αυτή τη στιγμή (Καθημερινή).")

