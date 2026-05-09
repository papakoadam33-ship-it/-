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
    .prob-text { font-size: 12px; color: #888; margin-bottom: 2px; }
    .tip-box { background: rgba(255,255,255,0.05); padding: 8px; border-radius: 8px; margin-top: 5px; }
    .update-box { background-color: #262730; padding: 10px; border-radius: 10px; text-align: center; border: 1px solid #3b82f6; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">⚽ Marios Pro-Bet Pro</div>', unsafe_allow_html=True)

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
            league = parts[0].strip().replace("Premier League", "ΠΡΕΜΙΕΡ ΛΙΓΚ").replace("Serie A", "ΣΕΡΙΕ Α").replace("Bundesliga", "ΜΠΟΥΝΤΕΣΛΙΓΚΑ").replace("Ligue 1", "ΛΙΓΚ 1").replace("Primera Division", "ΛΑ ΛΙΓΚΑ").replace("Copa Libertadores", "ΚΟΠΑ ΛΙΜΠΕΡΤΑΔΟΡΕΣ")
            
            # Ανάλυση Tips και Ποσοστών
            data = parts[2].split(",")
            t1, p1, t2, p2 = data[0], data[1], data[2], data[3]

            st.markdown(f"""
                <div class="match-card">
                    <div class="league">🏆 {league}</div>
                    <div class="teams">{parts[1].strip()}</div>
                    <div class="tip-box">
                        <div class="prob-text">🎯 Κύρια Επιλογή ({p1})</div>
                        <div style="font-weight:bold; color:#10b981; margin-bottom:8px;">{t1}</div>
                        <div class="prob-text">🛡️ Κάλυψη ({p2})</div>
                        <div style="font-weight:bold; color:#f59e0b;">{t2}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
