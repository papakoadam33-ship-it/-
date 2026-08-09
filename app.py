import os
import streamlit as st

st.set_page_config(
    page_title="MARIOS PRO-BET VIP", 
    page_icon="⚡", 
    layout="wide"
)

# --- ΔΙΕΥΡΥΜΕΝΟ ΛΕΞΙΚΟ ΜΕΤΑΦΡΑΣΕΩΝ ---
LEAGUE_TRANSLATIONS = {
    "Campeonato Brasileiro": "Πρωτάθλημα Βραζιλίας (Brasileirao) 🇧🇷",
    "Premier League": "Πρωτάθλημα Αγγλίας (Premier League) 🏴󠁧󠁢󠁥󠁮󠁧󠁿",
    "La Liga": "Πρωτάθλημα Ισπανίας (La Liga) 🇪🇸",
    "Serie A": "Πρωτάθλημα Ιταλίας (Serie A) 🇮🇹",
    "Bundesliga": "Πρωτάθλημα Γερμανίας (Bundesliga) 🇩🇪",
    "Ligue 1": "Πρωτάθλημα Γαλλίας (Ligue 1) 🇫🇷",
    "Primeira Liga": "Πρωτάθλημα Πορτογαλίας (Primeira Liga) 🇵🇹",
    "Eredivisie": "Πρωτάθλημα Ολλανδίας (Eredivisie) 🇳🇱",
    "Championship": "Β' Αγγλίας (Championship) 🏴󠁧󠁢󠁥󠁮󠁧󠁿",
    "UEFA Champions League Qualification": "Champions League (Προκριματικά) 🏆",
    "Leagues Cup": "Leagues Cup (MLS vs Mexico) 🌎",
    "Allsvenskan": "Πρωτάθλημα Σουηδίας (Allsvenskan) 🇸🇪",
    "Veikkausliiga": "Πρωτάθλημα Φινλανδίας (Veikkausliiga) 🇫🇮",
    "Liga Profesional": "Πρωτάθλημα Αργεντινής 🇦🇷",
    "Champions League": "Champions League 🏆",
    "Euro": "Euro 🇪🇺",
    "World Cup": "World Cup 🌎"
}

# --- ADVANCED VIP DARK CSS DESIGN ---
st.markdown("""
    <style>
    .stApp { background-color: #0F0F0F; color: #FFFFFF; }
    
    /* Header Container */
    .header-box {
        background: linear-gradient(135deg, #1E1E1E 0%, #111111 100%);
        padding: 25px; border-radius: 15px; text-align: center;
        border: 2px solid #FFD700; margin-bottom: 20px;
        box-shadow: 0px 4px 20px rgba(255, 215, 0, 0.25);
    }
    .header-title { font-size: 32px; font-weight: 900; color: #FFFFFF; letter-spacing: 1.5px; margin: 0; }
    .header-subtitle { font-size: 16px; font-style: italic; color: #FFD700; margin-top: 8px; }
    
    /* Date Badge */
    .date-badge {
        background-color: #1A1A1A; color: #FFD700; padding: 10px; border-radius: 8px;
        text-align: center; font-weight: bold; font-size: 15px; border: 1px solid #FFD700; margin-bottom: 20px;
    }
    
    /* Match Card */
    .match-card { 
        background-color: #161616; border: 1px solid #2A2A2A; 
        border-left: 6px solid #FFD700; border-radius: 12px; 
        padding: 18px; margin-bottom: 12px;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.5);
    }
    .league-label { color: #FCD34D; font-size: 13px; font-weight: bold; text-transform: uppercase; margin-bottom: 5px; }
    .teams-label { color: #FFFFFF; font-size: 19px; font-weight: bold; margin-bottom: 5px; }
    .time-badge { color: #9CA3AF; font-size: 13px; margin-bottom: 12px; }
    
    /* Prediction Row */
    .prediction-row { display: flex; gap: 8px; margin-bottom: 5px; flex-wrap: wrap; }
    .tip-main { background-color: #D4AF37; color: #000000; padding: 8px 12px; border-radius: 6px; font-weight: bold; font-size: 14px; flex: 1; min-width: 110px; text-align: center; }
    .pct-badge { background-color: #1F2937; color: #FCD34D; padding: 8px 12px; border-radius: 6px; font-weight: bold; font-size: 14px; border: 1px solid #374151; text-align: center; }
    .cover-badge { background-color: #111827; color: #9CA3AF; padding: 8px 12px; border-radius: 6px; font-size: 14px; border: 1px solid #1F2937; text-align: center; flex: 1; }
    
    /* Bet Slip Styling */
    .slip-box {
        background-color: #181818; border: 2px solid #10B981;
        border-radius: 12px; padding: 15px; margin-bottom: 20px;
    }
    .slip-title { color: #10B981; font-weight: bold; font-size: 18px; margin-bottom: 10px; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
    <div class="header-box">
        <div class="header-title">⚡ MARIOS PRO-BET VIP ⚡</div>
        <div class="header-subtitle">AI Poisson Model & Live Bet Calculator</div>
    </div>
""", unsafe_allow_html=True)

filename = "daily_predictions.txt"
match_found = False
timestamp = "Σήμερα"
matches_by_date = {}
past_results = []

# --- ΔΙΑΒΑΣΜΑ & ΟΜΑΔΟΠΟΙΗΣΗ ---
if os.path.exists(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readlines()
        if lines:
            first_line = lines[0].strip()
            if "--- ΠΡΟΓΝΩΣΤΙΚΑ" in first_line:
                timestamp = first_line.replace("--- ΠΡΟΓΝΩΣΤΙΚΑ ", "").replace(" ---", "")
            
            is_results_section = False
            for line in lines:
                clean_line = line.strip()
                if "ΠΡΟΣΦΑΤΑ ΑΠΟΤΕΛΕΣΜΑΤΑ" in clean_line:
                    is_results_section = True
                    continue
                if clean_line.startswith("---") or clean_line.startswith("ΛΙΓΚΑ") or not clean_line:
                    continue
                
                if is_results_section:
                    past_results.append(clean_line)
                else:
                    parts = clean_line.split("|")
                    if len(parts) >= 5:
                        match_found = True
                        time_info = parts[2].split(" ")
                        date_key = time_info[0] if len(time_info) > 0 else "Άλλη Ημέρα"
                        
                        if date_key not in matches_by_date:
                            matches_by_date[date_key] = []
                        matches_by_date[date_key].append(parts)
    except Exception:
        timestamp = "Σήμερα"

st.markdown(f'<div class="date-badge">📅 ΕΝΗΜΕΡΩΣΗ ΑΛΓΟΡΙΘΜΟΥ: {timestamp}</div>', unsafe_allow_html=True)

# Session State για το Δελτίο
if "selected_bets" not in st.session_state:
    st.session_state.selected_bets = []

# Layout: Κύριο μέρος (8 cols) & Δελτίο Ταμείου (4 cols)
main_col, slip_col = st.columns([2.2, 1])

with main_col:
    if match_found and matches_by_date:
        # --- SIDEBAR ΦΙΛΤΡΑ ---
        st.sidebar.header("⚙️ VIP Φίλτρα")
        high_value_only = st.sidebar.checkbox("🔥 Μόνο High Pick (>75%)")
        search_query = st.sidebar.text_input("🔍 Αναζήτηση Ομάδας", "").lower()

        all_leagues = set()
        for m_list in matches_by_date.values():
            for m in m_list:
                all_leagues.add(m[0])
        selected_league = st.sidebar.selectbox("🏆 Επιλογή Διοργάνωσης", ["Όλες"] + sorted(list(all_leagues)))

        # --- TABS ΗΜΕΡΩΝ & ΙΣΤΟΡΙΚΟΥ ---
        sorted_dates = sorted(list(matches_by_date.keys()))
        tab_titles = [f"📅 {d}" for d in sorted_dates] + ["📜 Αποτελέσματα / Ταμείο"]
        tabs = st.tabs(tab_titles)

        # 1. TABS ΑΓΩΝΩΝ
        for i, date_key in enumerate(sorted_dates):
            with tabs[i]:
                day_matches = matches_by_date[date_key]
                
                # Metrics Ημέρας
                pcts = [float(m[4].replace("%", "").strip()) for m in day_matches if m[4].replace("%", "").strip().replace(".", "").isdigit()]
                avg_pct = f"{sum(pcts)/len(pcts):.1f}%" if pcts else "N/A"
                max_pct = f"{max(pcts):.1f}%" if pcts else "N/A"
                
                m1, m2, m3 = st.columns(3)
                m1.metric("📊 Αγώνες", len(day_matches))
                m2.metric("🎯 Μέση Πιθανότητα", avg_pct)
                m3.metric("🔥 Top Pick %", max_pct)
                st.divider()

                rendered_count = 0
                for idx, parts in enumerate(day_matches):
                    league_raw = parts[0]
                    teams = parts[1]
                    match_time = parts[2]
                    tip = parts[3]
                    pct_str = parts[4]
                    cover = parts[5] if len(parts) > 5 else "-"
                    
                    try:
                        pct_val = float(pct_str.replace("%", "").strip())
                    except:
                        pct_val = 50.0

                    # Εφαρμογή Φίλτρων
                    if high_value_only and pct_val < 75.0:
                        continue
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
                                <div class="pct-badge">🎯 {pct_str}%</div>
                                <div class="cover-badge">🛡️ Κάλυψη: {cover}</div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

                    # Checkbox για προσθήκη στο Δελτίο
                    match_id = f"{teams}_{date_key}_{idx}"
                    is_selected = st.checkbox(f"➕ Προσθήκη στο Δελτίο ({teams})", key=match_id)
                    
                    bet_item = {"teams": teams, "tip": tip, "pct": pct_str}
                    if is_selected and bet_item not in st.session_state.selected_bets:
                        st.session_state.selected_bets.append(bet_item)
                    elif not is_selected and bet_item in st.session_state.selected_bets:
                        st.session_state.selected_bets.remove(bet_item)

                if rendered_count == 0:
                    st.warning("⚠️ Δεν βρέθηκαν αγώνες με τα επιλεγμένα φίλτρα.")

        # 2. TAB ΑΠΟΤΕΛΕΣΜΑΤΩΝ (HISTORY)
        with tabs[-1]:
            st.subheader("📜 Πρόσφατα Αποτελέσματα Αλγόριθμου")
            if past_results:
                for res in past_results:
                    if "ΤΑΜΕΙΟ" in res or "✅" in res:
                        st.success(f"🟢 {res}")
                    elif "Χάθηκε" in res or "❌" in res:
                        st.error(f"🔴 {res}")
                    else:
                        st.info(f"⚪ {res}")
            else:
                st.info("ℹ️ Δεν υπάρχουν καταγεγραμμένα πρόσφατα αποτελέσματα στο αρχείο.")
    else:
        st.info("ℹ️ Δεν υπάρχουν διαθέσιμα προγνωστικά.")

# --- ΔΕΛΤΙΟ ΤΑΜΕΙΟΥ (BET SLIP CALCULATOR) ---
with slip_col:
    st.markdown("""
        <div class="slip-box">
            <div class="slip-title">🎟️ ΨΗΦΙΑΚΟ ΔΕΛΤΙΟ</div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.selected_bets:
        st.write(f"**Επιλεγμένοι Αγώνες:** {len(st.session_state.selected_bets)}")
        
        estimated_odds = 1.0
        for b in st.session_state.selected_bets:
            st.info(f"⚽ **{b['teams']}**\n\n👉 Σημείο: `{b['tip']}` ({b['pct']})")
            # Εκτίμηση απόδοσης βάσει πιθανότητας
            try:
                p = float(b['pct'].replace("%", "").strip())
                odd = round(100 / p, 2) if p > 0 else 1.50
            except:
                odd = 1.50
            estimated_odds *= odd

        st.divider()
        st.write(f"📈 **Εκτιμώμενη Συνολική Απόδοση:** `{estimated_odds:.2f}`")
        
        stake = st.number_input("💰 Ποντάρισμα (€)", min_value=1.0, value=10.0, step=5.0)
        win = stake * estimated_odds
        
        st.success(f"💸 **Πιθανό Κέρδος:** `{win:.2f}€`")
        
        if st.button("🗑️ Καθαρισμός Δελτίου"):
            st.session_state.selected_bets = []
            st.rerun()
    else:
        st.write("Τσεκάρισε το **«Προσθήκη στο Δελτίο»** κάτω από κάθε ματς για να υπολογίσεις το ποντάρισμά σου!")
