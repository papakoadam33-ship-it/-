import streamlit as st
import os
from datetime import datetime

st.set_page_config(page_title="Marios Pro-Bet Pro", page_icon="📈")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .main-title { font-size: 30px; font-weight: bold; text-align: center; margin-bottom: 5px; color: #ffffff; }
    .sub-title { text-align: center; color: #10b981; font-size: 16px; margin-bottom: 20px; }
    
    .match-card {
        background-color: #1f2937;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 12px;
        border-left: 6px solid #10b981;
    }
    .league-row { display: flex; justify-content: space-between; align-items: center; }
    .league-name { color: #3b82f6; font-size: 12px; font-weight: bold; text-transform: uppercase; }
    .match-time { color: #facc15; font-size: 12px; font-weight: bold; background: rgba(250, 204, 21, 0.1); padding: 2px 8px; border-radius: 5px; }
    .teams { font-size: 17px; font-weight: bold; color: white; margin: 10px 0; }
    .tip-box { background: rgba(255,255,255,0.05); padding: 10px; border-radius: 8px; }
    .prob-text { font-size: 11px; color: #aaa; margin-bottom: 2px; }
    .update-box { background-color: #262730; padding: 10px; border-radius: 10px; text-align: center; border: 1px solid #3b82f6; margin-bottom: 20px; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">⚽ Marios Pro-Bet Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Statistical Match Analysis</div>', unsafe_allow_html=True)

if os.path.exists("daily_predictions.txt"):
    with open("daily_predictions.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    for line in lines:
        line = line.strip()
        if not line or "|" not in line: continue
        
        parts = line.split("|")
        if line.startswith("ΗΜΕΡΟΜΗΝΙΑ"):
            st.markdown(f'<div class="update-box">📅 {parts[1]} | ⏰ {parts[2]}</div>', unsafe_allow_html=True)
        elif len(parts) == 3:
            # Διαχωρισμός Λίγκας και Ώρας (π.χ. "SERIE A (21:45)")
            league_part = parts[0].strip()
            display_time = ""
            if "(" in league_part:
                display_time = league_part[league_part.find("(")+1:league_part.find(")")]
                league_part = league_part.split("(")[0].strip()

            # Μεταφράσεις
            league_final = league_part.replace("Premier League", "ΠΡΕΜΙΕΡ ΛΙΓΚ").replace("Serie A", "ΣΕΡΙΕ Α").replace("Bundesliga", "ΜΠΟΥΝΤΕΣΛΙΓΚΑ").replace("Ligue 1", "ΛΙΓΚ 1").replace("Campeonato Brasileiro Série A", "ΒΡΑΖΙΛΙΑ").replace("Championship", "ΤΣΑΜΠΙΟΝΣΙΠ")
            
            # Tips & Probs
            data = parts[2].split(",")
            if len(data) >= 4:
                t1, p1, t2, p2 = data[0], data[1], data[2], data[3]

                st.markdown(f"""
                    <div class="match-card">
                        <div class="league-row">
                            <div class="league-name">🏆 {league_final}</div>
                            <div class="match-time">🕒 {display_time}</div>
                        </div>
                        <div class="teams">{parts[1].strip()}</div>
                        <div class="tip-box">
                            <div style="display: flex; justify-content: space-between;">
                                <div>
                                    <div class="prob-text">🎯 Κύρια ({p1})</div>
                                    <div style="font-weight:bold; color:#10b981; font-size:16px;">{t1}</div>
                                </div>
                                <div style="text-align: right;">
                                    <div class="prob-text">🛡️ Κάλυψη ({p2})</div>
                                    <div style="font-weight:bold; color:#f59e0b; font-size:16px;">{t2}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
