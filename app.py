
matches = get_football_data()

if matches:
    # Δημιουργία λίστας για φίλτρο διοργανώσεων
    leagues = sorted(list(set([m['competition']['name'] for m in matches])))
    selected_league = st.sidebar.selectbox("🏆 Επιλογή Διοργάνωσης", ["Όλες οι Λίγκες"] + leagues)

    # Φιλτράρισμα
    display_count = 0
    for m in matches:
        league = m['competition']['name']
        home = m['homeTeam']['name']
        away = m['awayTeam']['name']
        status = m['status']
        
        # Λογική φίλτρων
        if (selected_league == "Όλες οι Λίγκες" or selected_league == league) and \
           (search.lower() in home.lower() or search.lower() in away.lower()):
            
            display_count += 1
            tip = generate_tip(league)
            
            # Διαχείριση Live Σκορ
            score_html = ""
            if status == "IN_PLAY":
                h_score = m['score']['fullTime']['home']
                a_score = m['score']['fullTime']['away']
                score_html = f"<span class='live-tag'> ● LIVE: {h_score} - {a_score}</span>"
            elif status == "FINISHED":
                h_score = m['score']['fullTime']['home']
                a_score = m['score']['fullTime']['away']
                score_html = f"<span style='color:#8892b0; font-size:0.9rem;'> (Τελικό: {h_score}-{a_score})</span>"

            # Εμφάνιση Κάρτας
            st.markdown(f"""
                <div class="prediction-card">
                    <div class="league-label">🏆 {league}</div>
                    <div class="match-title">{home} vs {away} {score_html}</div>
                    <div class="tip-container">
                        <span class="tip-icon">🎯</span>
                        <span class="tip-text">Πρόβλεψη: {tip}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            if display_count >= 40: break

    if display_count == 0:
        st.warning("Δεν βρέθηκαν αγώνες για τα κριτήρια που θέσατε.")
else:
    st.error("⚠️ Πρόβλημα στη λήψη δεδομένων. Δοκιμάστε ξανά σε λίγο.")

st.markdown("---")
st.caption("© 2026 Marios Pro-Bet | Powered by Football-Data.org API")
