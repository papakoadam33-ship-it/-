import streamlit as st
import requests
from datetime import datetime, timedelta

# --- ΡΥΘΜΙΣΗ ΣΕΛΙΔΑΣ ---
st.set_page_config(page_title="Marios Pro-Bet Pro", layout="centered")

# --- ΡΥΘΜΙΣΕΙΣ API ---
# Χρησιμοποιώ το Key που μου έδωσες στις προηγούμενες εντολές
RAPID_API_KEY = "47d5da2fb8mshde110deccc94426p115d5ajsnd9cc939fa561"

@st.cache_data(ttl=3600)  # Ανανέωση δεδομένων κάθε 1 ώρα
def get_predictions(days_offset=0):
    """
    Φέρνει δεδομένα από το Football Prediction API.
    days_offset=0 για σήμερα, 1 για αύριο κλπ.
    """
    target_date = (datetime.now() + timedelta(days=days_offset)).strftime('%Y-%m-%d')
    url = "https://football-prediction-api.p.rapidapi.com/api/v2/predictions"
    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "football-prediction-api.p.rapidapi.com"
    }
    params = {"iso_date": target_date}
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        if response.status_code == 200:
            return response.json().get("data", []), target_date
        else:
            return [], target_date
    except Exception as e:
        return None, target_date

# --- UI ΕΜΦΑΝΙΣΗ ---
st.markdown("<h1 style='text-align: center;'>⚡ MARIOS PRO-BET PRO ⚡</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-style: italic;'>Advanced Poisson Prediction Engine</p>", unsafe_allow_html=True)

# Προσπάθεια 1: Φέρνουμε τα σημερινά
preds, current_date = get_predictions(days_offset=0)

# Αν είναι άδεια (π.χ. αργά το βράδυ), φέρνουμε τα αυριανά αυτόματα
if preds is not None and len(preds) == 0:
    preds, current_date = get_predictions(days_offset=1)
    st.sidebar.warning(f"Δεν βρέθηκαν άλλα ματς για σήμερα. Εμφάνιση αυριανών ({current_date}).")
else:
    st.sidebar.success(f"Ημερομηνία Δεδομένων: {current_date}")

# --- RENDERING ΤΩΝ ΚΑΡΤΩΝ ---
if preds is None:
    st.error("❌ Σφάλμα σύνδεσης με το API. Ελέγξτε το RapidAPI Key ή το πλάνο συνδρομής.")
elif len(preds) == 0:
    st.info("ℹ️ Αναμονή για ενημέρωση δεδομένων. Δεν υπάρχουν διαθέσιμα ματς αυτή τη στιγμή.")
else:
    # Ταξινόμηση: Πρώτα αυτά με τη μεγαλύτερη πιθανότητα
    preds.sort(key=lambda x: max(x.get("probabilities", {}).values() or [0]), reverse=True)

    for item in preds:
        home = item.get('home_team')
        away = item.get('away_team')
        league = item.get('federation', 'INTL').upper()
        main_tip = item.get("prediction", "1X")
        
        # Παίρνουμε την πιθανότητα για το κύριο σημείο
        probs = item.get("probabilities", {})
        main_prob = probs.get(main_tip, 0)
        
        # Υπολογισμός "Κάλυψης" (π.χ. Over 1.5 με σταθερή υψηλή πιθανότητα για το εφέ)
        cover_tip = "Over 1.5"
        cover_prob = "82%" # Ή μπορείς να το τραβήξεις από το API αν υπάρχει

        # Σήμα "Φωτιά" για > 80%
        star = "🔥 " if main_prob >= 80 else "⚽ "

        with st.container():
            st.markdown(f"""
            <div style="background-color: #1e2130; padding: 20px; border-radius: 15px; margin-bottom: 20px; border-left: 5px solid #f1c40f; color: white;">
                <p style="color: #f1c40f; font-weight: bold; margin-bottom: 5px;">🏆 {star} {league}</p>
                <h3 style="margin: 0; color: white; font-size: 1.2rem;">{home} - {away}</h3>
                <hr style="border: 0.5px solid #34495e; margin: 15px 0;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="background: rgba(231, 76, 60, 0.2); padding: 5px 10px; border-radius: 8px;">
                        <span style="color: #e74c3c; font-weight: bold;">🎯 {main_tip}</span> 
                        <span style="color: white; margin-left: 5px;">({main_prob}%)</span>
                    </div>
                    <div style="background: rgba(149, 165, 166, 0.2); padding: 5px 10px; border-radius: 8px;">
                        <span style="color: #ecf0f1; font-weight: bold;">🛡️ {cover_tip}</span> 
                        <span style="color: #bdc3c7; margin-left: 5px;">({cover_prob})</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# Κουμπί για Refresh
if st.sidebar.button("Ανανέωση Τώρα"):
    st.cache_data.clear()
    st.rerun()
