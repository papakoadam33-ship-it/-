import streamlit as st
import os

st.set_page_config(page_title="MARIOS PRO-BET", page_icon="⚡", layout="centered")

# --- ΔΙΕΥΡΥΜΕΝΟ ΛΕΞΙΚΟ ΜΕΤΑΦΡΑΣΕΩΝ ---
LEAGUE_TRANSLATIONS = {
    "Campeonato Brasileiro": "Πρωτάθλημα Βραζιλίας (Brasileirao) 🇧🇷",
    "Premier League": "Πρωτάθλημα Αγγλίας (Premier League) 🏴󠁧󠁢󠁥󠁮󠁧󠁿",
    "La Liga": "Πρωτάθλημα Ισπανίας (La Liga) 🇪🇸",
    "Serie A": "Πρωτάθλημα Ιταλίας (Serie A) 🇮🇹",
    "Bundesliga": "Πρωτάθλημα Γερμανίας (Bundesliga) 🇩🇪",
    "Ligue 1": "Πρωτάθλημα Γαλλίας (Ligue 1) 🇫🇷",
    "UEFA Champions League Qualification": "Champions League (Προκριματικά) 🏆",
    "Leagues Cup": "Leagues Cup (MLS vs Mexico) 🌎",
    "Allsvenskan": "Πρωτάθλημα Σουηδίας (Allsvenskan) 🇸🇪",
    "Veikkausliiga": "Πρωτάθλημα Φινλανδίας (Veikkausliiga) 🇫🇮",
    "Liga Profesional": "Πρωτάθλημα Αργεντινής 🇦🇷",
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
    .match-card { background-color: #1A1A1A; border: 1px solid #333333; border-left: 5px solid #FFD700; border-radius: 12px; padding: 20px; margin-bottom: 10px; }
    .league-label { color: #FCD34D; font-size: 13px; font-weight: bold; text-transform: uppercase; margin-bottom: 5px; }
    .teams-label { color: #FFFFFF; font-size: 20px; font-weight: bold; margin-bottom: 5px; }
    .time-badge { color: #9CA3AF; font-size: 13px; margin-bottom: 15px; }
    
    /* Σειρά Προγνωστικών */
    .prediction-row { display: flex; gap: 10px; margin-bottom: 5px; flex-wrap: wrap; }
    .tip-main { background-color: #CCA43B; color: #000000; padding: 8px 15px; border-radius: 6px; font-weight: bold; font-size: 15px; flex: 1; min-width: 120px; text-align: center; }
    .pct-badge { background-color: #1F2937; color: #FCD34D; padding: 8px 15px; border-radius: 6px; font-weight: bold; font-size: 15px; border: 1px solid #374151; text-align: center; }
    .cover-badge { background-color: #111827; color: #9CA3AF; padding: 8px 15px; border-radius: 6px; font-size: 15px; border: 1px solid #1F2937; text-align: center; flex: 1; }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
    <div class="header-box">
        <div class="header-title">⚡ MARIOS PRO-BET PRO ⚡</div>
        <div class="header-subtitle">Daily AI & Poisson Distribution Model</div>
    </div>
""", unsafe_allow_html=True)

filename = "daily_predictions.txt"
match_found = False
timestamp = "Σήμερα"
matches_to_render = []

# --- ΔΙΑΒΑΣΜΑ ΑΡΧΕΙΟΥ ---
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
                if len(parts) >= 5:
                    matches_to_render.append(parts)
                    match_found = True
    except Exception:
        timestamp = "Σήμερα"

st.markdown(f'<div class="date-badge">📅 ΣΗΜΕΡΙΝΑ ΠΡΟΓΝΩΣΤΙΚΑ: {timestamp}</div>', unsafe_allow_html=True)

# --- SIDEBAR (ΦΙΛΤΡΑ & ΑΝΑΖΗΤΗΣΗ) ---
st.sidebar.header("🔍 Φίλτρα & Αναζήτηση")
search_query = st.sidebar.text_input("Αναζήτηση Ομάδας", "").lower()

all_leagues = list(set([m[0] for m in matches_to_render])) if match_found else []
selected_league = st.sidebar.selectbox("Επιλογή Διοργάνωσης", ["Όλες"] + all_leagues)

# --- METRICS DASHBOARD (ΣΤΑΤΙΣΤΙΚΑ ΗΜΕΡΑΣ) ---
if match_found:
    col1, col2, col3 = st.columns(3)
    col1.metric("📊 Σύνολο Αγώνων", len(matches_to_render))
    
    # Υπολογισμός μέσου όρου πιθανότητας
    pcts = [float(m[4].replace("%", "").strip()) for m in matches_to_render if m[4].replace("%", "").strip().replace(".", "").isdigit()]
    avg_pct = f"{sum(pcts)/len(pcts):.1f}%" if pcts else "N/A"
    max_pct = f"{max(pcts):.1f}%" if pcts else "N/A"
    
    col2.metric("🎯 Μέση Πιθανότητα", avg_pct)
    col3.metric("🔥 Top Pick %", max_pct)
    st.divider()

st.markdown('<div class="vip-section-title">🔥 ΗΜΕΡΗΣΙΑ VIP PICKS</div>', unsafe_allow_html=True)

# --- DISPLAY MATCHES ---
rendered_count = 0
if match_found:
    for parts in matches_to_render:
        league_raw = parts[0]
        teams = parts[1]
        match_time = parts[2]
        tip = parts[3]
        pct = parts[4]
        cover = parts[5] if len(parts) > 5 else "-"
        
        # Εφαρμογή Φίλτρων
        if selected_league != "Όλες" and league_raw != selected_league:
            continue
        if search_query and search_query not in teams.lower():
            continue

        rendered_count += 1
        
        # Κάρτα Αγώνα
        st.markdown(f"""
            <div class="match-card">
                <div class="league-label">🏆 {LEAGUE_TRANSLATIONS.get(league_raw, league_raw)}</div>
                <div class="teams-label">{teams}</div>
                <div class="time-badge">🕒 {match_time}</div>
                <div class="prediction-row">
                    <div class="tip-main">👑 {tip}</div>
                    <div class="pct-badge">🎯 {pct}%</div>
                    <div class="cover-badge">🛡️ Κάλυψη: {cover}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Δωρεάν Interactive Expander για κάθε ματς
        with st.expander(f"📊 Ανάλυση & Copy Tip για {teams}"):
            st.write(f"**Μοντέλο Υπολογισμού:** Poisson Algorithm v2.4")
            st.write(f"**Εκτιμώμενη Αξία (Value):** HIGH ✅")
            st.code(f"{teams} -> {tip} (@{pct}%)", language="text")

if rendered_count == 0 and match_found:
    st.warning("⚠️ Δεν βρέθηκαν αγώνες με τα κριτήρια αναζήτησης που έβαλες.")
elif not match_found:
    st.info("ℹ️ Δεν υπάρχουν διαθέσιμα σημερινά προγνωστικά. Μόλις ο scraper ανανεώσει το daily_predictions.txt, θα εμφανιστούν αυτόματα εδώ.")
