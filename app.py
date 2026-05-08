import streamlit as st
import os

st.set_page_config(page_title="Marios Pro-Bet", page_icon="⚽")

# Το CSS για την "Βιτρίνα"
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .match-card {
        background-color: #1f2937;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 12px;
        border-left: 6px solid #10b981;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .league-name { color: #3b82f6; font-weight: bold; font-size: 14px; margin-bottom: 5px; }
    .team-names { font-size: 17px; font-weight: 600; color: #f3f4f6; margin: 8px 0; }
    .tip-style { 
        background: rgba(16, 185, 129, 0.2); 
        color: #10b981; 
        padding: 6px 12px; 
        border-radius: 6px; 
        font-weight: bold; 
        display: inline-block;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>⚽ Marios Pro-Bet</h1>", unsafe_allow_html=True)

if os.path.exists("daily_predictions.txt"):
    with open("daily_predictions.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    current_league = ""
    
    for line in lines:
        line = line.strip()
        if not line or "===" in line or "MARIOS PRO" in line or line.startswith("---"):
            continue
            
        if "Ενημέρωση" in line:
            st.info(f"📅 {line}")
        elif "🏆" in line:
            current_league = line.replace("🏆", "").strip()
        elif "➔" in line or "Προγνωστικό:" in line:
            # Διαχωρισμός ομάδων και tips
            if "➔" in line:
                parts = line.split("➔")
            else:
                parts = line.split("Προγνωστικό:")
                
            teams = parts[0].replace("⚽", "").replace("🔹", "").strip()
            tip = parts[1].strip()
            
            # Εμφάνιση Κάρτας
            st.markdown(f"""
                <div class="match-card">
                    <div class="league-name">🏆 {current_league}</div>
                    <div class="team-names">{teams}</div>
                    <div class="tip-style">🎯 {tip}</div>
                </div>
            """, unsafe_allow_html=True)
else:
    st.error("Αναμονή για δεδομένα...")
