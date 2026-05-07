import streamlit as st
import requests
from datetime import datetime
import time

# Ρύθμιση σελίδας
st.set_page_config(page_title="Marios Pro-Bet", page_icon="⚽")

# --- ΤΙΤΛΟΣ ---
st.title("⚽ Marios Pro-Bet")
st.markdown("---")

# Το κλειδί σου (Ενσωματωμένο)
API_KEY = "47d5da2fb8mshde110deccc94426p115d5ajsnd9cc939fa561"

HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

# IDs Πρωταθλημάτων: Αγγλία, Ισπανία, Ιταλία, Βραζιλία, Αργεντινή, Πορτογαλία, Ελλάδα
LEAGUE_IDS = [39, 140, 135, 71, 128, 94, 197]

def get_predictions():
    fixtures_url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    today = datetime.now().strftime('%Y-%m-%d')
    
    found_any_league = False
    
    for league_id in LEAGUE_IDS:
        params = {"league": str(league_id), "date": today}
        
        try:
            response = requests.get(fixtures_url, headers=HEADERS, params=params)
            data = response.json()
            matches = data.get('response', [])
            
            if matches:
                found_any_league = True
                league_name = matches[0]['league']['name']
                st.header(f"🏆 {league_name}")
                
                for m in matches:
                    home = m['teams']['home']['name']
                    away = m['teams']['away']['name']
                    fixture_id = m['fixture']['id']
                    status = m['fixture']['status']['long']
                    
                    with st.expander(f"🏟️ {home} vs {away} ({status})"):
                        # Λήψη Προγνωστικού
                        pred_url = "https://api-football-v1.p.rapidapi.com/v3/predictions"
                        p_res = requests.get(pred_url, headers=HEADERS, params={"fixture": fixture_id})
                        p_data = p_res.json()
                        
                        if p_data.get('response'):
                            prediction = p_data['response'][0]['predictions']
                            advice = prediction['advice']
                            percents = prediction['percent']
                            
                            st.success(f"**🎯 Tip: {advice}**")
                            
                            # Εμφάνιση Ποσοστών
                            col1, col2, col3 = st.columns(3)
                            col1.metric("1 (Home)", percents['home'])
                            col2.metric("X (Draw)", percents['draw'])
                            col3.metric("2 (Away)", percents['away'])
                        else:
                            st.warning("⚠️ Δεν υπάρχουν διαθέσιμα στατιστικά γι' αυτόν τον αγώνα.")
                        
                        # Μικρή καθυστέρηση για να μην μπλοκάρει το API (Rate Limit)
                        time.sleep(1)
            
        except Exception as e:
            st.error(f"Σφάλμα σύνδεσης: {e}")

    if not found_any_league:
        st.info("📅 Δεν βρέθηκαν αγώνες για σήμερα στα επιλεγμένα πρωταθλήματα. Δοκίμασε ξανά αργότερα!")

# ΚΟΥΜΠΙ ΓΙΑ ΕΝΑΡΞΗ
if st.button('🚀 Λήψη Προγνωστικών'):
    with st.status("Αναζήτηση αγώνων και ανάλυση δεδομένων...", expanded=True) as status:
        get_predictions()
        status.update(label="Η ανάλυση ολοκληρώθηκε!", state="complete", expanded=False)

st.markdown("---")
st.caption("Powered by API-Football • Created for Marios Pro-Bet")

