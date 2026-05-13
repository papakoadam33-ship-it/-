import streamlit as st
import os

# --- 1. ΡΥΘΜΙΣΗ ΣΕΛΙΔΑΣ ---
st.set_page_config(page_title="Marios Pro-Bet Pro", layout="centered", page_icon="⚡")

# --- 2. CSS STYLING ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    h1 { color: #f1c40f; text-align: center; font-size: 38px !important; text-shadow: 2px 2px #000; font-weight: bold; padding-bottom: 20px; }
    
    .info-container {
        background-color: #1a1c23;
        border: 2px solid #f1c40f;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        color: #f1c40f;
        font-weight: bold;
        margin-bottom: 25px;
    }

    .prediction-card {
        background-color: #1a1c23;
        border: 1px solid #f1c40f;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        position: relative;
    }
    .league-title { color: #f1c40f; font-weight: bold; font-size: 16px; text-transform: uppercase; }
    .teams-title { color: #ffffff; font-size: 22px; font-weight: bold; margin: 10px 0; }
    .time-badge {
        background-color: #e74c3c;
        color: white;
        padding: 4px 10px;
        border-radius: 6px;
        float: right;
        font-weight: bold;
        font-size: 14px;
    }
    .tip-box {
        display: inline-block;
        padding: 10px 15px;
        border-radius: 10px;
        margin-top: 10px;
        font-weight: bold;
        text-align: center;
    }
    .main-tip { background-color: #27ae60; color: white; margin-right: 10px; border: 1px solid #2ecc71; }
    .cover-tip { background-color: #d35400; color: white; border: 1px solid #e67e22; }
    
    /* Responsive fixes */
    @media (max-width: 600px) {
        .time-badge { float: none; display: block; width: fit-content; margin-bottom: 10px; }
        .tip-box { display: block; margin-right: 0; width: 100%; margin-bottom: 5px; }
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ΤΙΤΛΟΣ ---
st.markdown("<h1>⚡ MARIOS PRO-BET PRO ⚡</h1>", unsafe_allow_html=True)

# --- 4. ΑΝΑΓΝΩΣΗ ΔΕΔΟΜΕΝΩΝ ---
FILE_NAME = "daily_predictions.txt"

if not os.path.exists(FILE_NAME):
    st.error(f"❌ Το αρχείο {FILE_NAME} δεν βρέθηκε στο repository.")
    st.info("Σιγουρέψου ότι το GitHub Action έχει ολοκληρωθεί επιτυχώς.")
else:
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
            
        if len(lines) > 2:
            # Η πρώτη γραμμή είναι ο τίτλος (π.χ. --- ΠΡΟΓΝΩΣΤΙΚΑ 13/05/2026 ---)
            raw_header = lines[0].replace("-", "").strip()
            
            st.markdown(f"""
            <div class="info-container">
                📅 {raw_header}
            </div>
            """, unsafe_allow_html=True)
            
            # Ξεκινάμε από την 3η γραμμή (index 2) για να προσπεράσουμε τον τίτλο και τα headers
            for line in lines[2:]:
                parts = line.split("|")
                if len(parts) >= 5:
                    league, teams, m_time, main_tip, cover_tip = parts
                    
                    st.markdown(f"""
                    <div class="prediction-card">
                        <span class="time-badge">🕒 {m_time}</span>
                        <div class="league-title">🏆 {league}</div>
                        <div class="teams-title">{teams}</div>
                        <div class="tip-box main-tip">🎯 {main_tip}</div>
                        <div class="tip-box cover-tip">🛡️ {cover_tip}</div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ Το αρχείο βρέθηκε αλλά δεν περιέχει ακόμα προγνωστικά.")
            
    except Exception as e:
        st.error(f"⚠️ Σφάλμα κατά την επεξεργασία: {e}")

# --- 5. FOOTER ---
st.markdown("<br><p style='text-align: center; color: gray; font-size: 12px;'>Powered by Python & Football-Data API</p>", unsafe_allow_html=True)
