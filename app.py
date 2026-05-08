import streamlit as st
import os

st.set_page_config(page_title="Marios Pro-Bet", page_icon="⚽")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .main-title { font-size: 28px; font-weight: bold; text-align: center; margin-bottom: 20px; color: #ffffff; }
    .match-card {
        background-color: #1f2937;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 12px;
        border-left: 6px solid #10b981;
    }
    .league { color: #3b82f6; font-size: 13px; font-weight: bold; text-transform: uppercase; }
    .teams { font-size: 16px; font-weight: bold; color: white; margin: 5px 0; }
    .tip-container { display: flex; gap: 10px; margin-top: 8px; }
    .tip1 { color: #10b981; font-weight: bold; background: rgba(16, 185, 129, 0.1); padding: 5px 10px; border-radius: 5px; font-size: 14px; border: 1px solid #10b981; }
    .tip2 { color: #f59e0b; font-weight: bold; background: rgba(245, 158, 11, 0.1); padding: 5px 10px; border-radius: 5px; font-size: 14px; border: 1px solid #f59e0b; }
    .update-box { background-color: #262730; padding: 10px; border-radius: 10px; text-align: center; border: 1px solid #3b82f6; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">⚽ Marios Pro-Bet</div>', unsafe_allow_html=True)

if os.path.exists("daily_predictions.txt"):
    with open("daily_predictions.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    for line in lines:
        line = line.strip()
        if not line or "|" not in line: continue
        
        parts = line.split("|")
        if line.startswith("ΗΜΕΡΟΜΗΝΙΑ"):
            st.markdown(f'<div class="update-box">📅 <b>{parts[1]}</b> <span style="margin-left:10px;">⏰</span> <b>{parts[2]}</b></div>', unsafe_allow_html=True)
        elif len(parts) == 3:
            # Μεταφράσεις
            league = parts[0].strip().replace("Premier League", "ΠΡΕΜΙΕΡ ΛΙΓΚ").replace("Serie A", "ΣΕΡΙΕ Α").replace("Bundesliga", "ΜΠΟΥΝΤΕΣΛΙΓΚΑ").replace("Ligue 1", "ΛΙΓΚ 1").replace("Primera Division", "ΛΑ ΛΙΓΚΑ").replace("Copa Libertadores", "ΚΟΠΑ ΛΙΜΠΕΡΤΑΔΟΡΕΣ")
            
            # Χωρίζουμε τα δύο tips
            tips = parts[2].split(",")
            t1 = tips[0].strip()
            t2 = tips[1].strip() if len(tips) > 1 else ""

            st.markdown(f"""
                <div class="match-card">
                    <div class="league">🏆 {league}</div>
                    <div class="teams">{parts[1].strip()}</div>
                    <div class="tip-container">
                        <div class="tip1">🎯 {t1}</div>
                        <div class="tip2">🛡️ {t2}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

