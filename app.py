import streamlit as st
import os

st.set_page_config(page_title="Marios Pro-Bet", page_icon="⚽")

st.markdown("""
    <style>
    .match-card {
        background-color: #1f2937;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
        border-left: 6px solid #10b981;
    }
    .league-label { color: #3b82f6; font-size: 12px; font-weight: bold; text-transform: uppercase; }
    .team-text { font-size: 18px; font-weight: bold; color: white; margin: 10px 0; }
    .tip-text { color: #10b981; font-weight: bold; background: rgba(16, 185, 129, 0.1); padding: 8px; border-radius: 8px; display: inline-block; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚽ Marios Pro-Bet")

if os.path.exists("daily_predictions.txt"):
    with open("daily_predictions.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    current_league = "Διάφορα"
    
    for line in lines:
        line = line.strip()
        if not line or "===" in line or "MARIOS PRO" in line: continue
        
        if "Ενημέρωση" in line:
            st.info(f"📅 {line}")
        elif "🏆" in line:
            current_league = line.replace("🏆", "").strip()
        elif "➔" in line or "Προγνωστικό:" in line:
            # Πιάνει όλους τους αγώνες, ακόμα κι αν είναι σε μία γραμμή
            separator = "➔" if "➔" in line else "Προγνωστικό:"
            parts = line.split(separator)
            teams = parts[0].replace("⚽", "").replace("🔹", "").strip()
            tip = parts[1].strip()
            
            st.markdown(f'''
                <div class="match-card">
                    <div class="league-label">{current_league}</div>
                    <div class="team-text">{teams}</div>
                    <div class="tip-text">🎯 {tip}</div>
                </div>
            ''', unsafe_allow_html=True)
else:
    st.write("Ανανέωση δεδομένων...")

