import streamlit as st
import os

# Ρύθμιση της σελίδας
st.set_page_config(page_title="Marios Pro-Bet Pro", page_icon="⚡", layout="centered")

# Στυλ για όμορφη εμφάνιση (Dark Mode)
st.markdown("""
    <style>
    .main { background-color: #121212; }
    .title-text { text-align: center; color: #FFFFFF; font-size: 36px; font-weight: bold; margin-bottom: 20px; }
    .time-banner { background-color: #1E1E24; padding: 10px; border-radius: 10px; border: 2px solid #FFD700; text-align: center; color: #FFD700; font-size: 18px; font-weight: bold; margin-bottom: 25px; }
    .match-box { background-color: #1E1E1E; padding: 15px; border-radius: 15px; border: 1px solid #333333; margin-bottom: 15px; box-shadow: 2px 2px 10px rgba(0,0,0,0.5); }
    .league-title { color: #888888; font-size: 12px; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; }
    .teams-title { color: #FFFFFF; font-size: 20px; font-weight: bold; margin: 5px 0; }
    .time-badge { background-color: #D9534F; color: white; padding: 3px 8px; border-radius: 5px; font-size: 12px; font-weight: bold; display: inline-block; }
    .tip-box { background-color: #5CB85C; color: white; padding: 10px; border-radius: 8px; text-align: center; font-weight: bold; margin-top: 10px; font-size: 16px; }
    .cover-box { background-color: #F0AD4E; color: white; padding: 10px; border-radius: 8px; text-align: center; font-weight: bold; margin-top: 5px; font-size: 15px; }
    .info-box { background-color: #1E1E24; padding: 20px; border-radius: 15px; border: 2px solid #FFD700; text-align: center; margin-bottom: 15px; }
    .info-text { color: #FFFFFF; font-size: 22px; font-weight: bold; margin: 15px 0; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='title-text'>⚡ MARIOS PRO-BET PRO ⚡</div>", unsafe_allow_html=True)

filename = "daily_predictions.txt"

if os.path.exists(filename):
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    if lines:
        # Παίρνουμε την ημερομηνία από την πρώτη γραμμή
        timestamp = lines[0].replace("--- ΠΡΟΓΝΩΣΤΙΚΑ ", "").replace(" ---", "").strip()
        st.markdown(f"<div class='time-banner'>📅 ΠΡΟΓΝΩΣΤΙΚΑ {timestamp}</div>", unsafe_allow_html=True)
        
        # Διαβάζουμε τους αγώνες (παρακάμπτοντας τις 2 πρώτες γραμμές επικεφαλίδας)
        match_lines = lines[2:]
        
        # Έλεγχος αν υπάρχει μήνυμα INFO ή αν είναι άδεια η λίστα
        if not match_lines or "INFO" in match_lines[0]:
            st.markdown("""
                <div class='info-box'>
                    <span style='font-size: 30px;'>⏰</span>
                    <div class='info-text'>Αναμονή για ενημέρωση αγώνων...</div>
                    <div style='color: #888888;'>Το σύστημα ανανεώνει τις προβλέψεις αυτόματα κάθε 12 ώρες.</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            for line in match_lines:
                if "|" in line:
                    parts = line.strip().split("|")
                    if len(parts) >= 5:
                        league, match_name, match_time, tip, cover = parts[0], parts[1], parts[2], parts[3], parts[4]
                        
                        st.markdown(f"""
                            <div class='match-box'>
                                <div class='league-title'>🏆 {league}</div>
                                <div class='teams-title'>{match_name}</div>
                                <div class='time-badge'>🕒 {match_time}</div>
                                <div class='tip-box'>🎯 {tip}</div>
                                <div class='cover-box'>🛡️ {cover}</div>
                            </div>
                        """, unsafe_allow_html=True)
else:
    st.markdown("<div class='time-banner'>📅 ΠΡΟΓΝΩΣΤΙΚΑ --/--/---- --:--</div>", unsafe_allow_html=True)
    st.info("Δεν έχει δημιουργηθεί ακόμα το αρχείο προβλέψεων. Παρακαλώ περιμένετε να τρέξει το GitHub Action.")

st.markdown("<p style='text-align: center; color: #555555; font-size: 12px; margin-top: 5px;'>Powered by Python & Football-Data API</p>", unsafe_allow_html=True)
