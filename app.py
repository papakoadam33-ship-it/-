import streamlit as st
import os

st.set_page_config(page_title="Marios Pro-Bet", page_icon="⚽")

# Custom CSS για να μην χαλάει ποτέ η εμφάνιση
st.markdown("""
    <style>
    .match-card {
        background-color: #262730;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 10px;
        border-left: 5px solid #00ff00;
        color: white;
    }
    .league-title { color: #007bff; font-weight: bold; font-size: 14px; }
    .team-names { font-size: 18px; margin: 5px 0; }
    .prediction { color: #00ff00; font-weight: bold; background: rgba(0,255,0,0.1); padding: 5px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚽ Marios Pro-Bet")

if os.path.exists("daily_predictions.txt"):
    with open("daily_predictions.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    current_league = "Γενικά"
    
    for line in lines:
        line = line.strip()
        if not line or "===" in line or "MARIOS PRO" in line:
            continue
            
        if "🏆" in line:
            current_league = line.replace("🏆", "")
        elif "➔" in line or "->" in line:
            # Εδώ είναι το μυστικό: Χωρίζουμε τη γραμμή στο βέλος
            separator = "➔" if "➔" in line else "->"
            parts = line.split(separator)
            teams = parts[0].replace("⚽", "").replace("🔹", "").strip()
            tip = parts[1].strip()
            
            # Φτιάχνουμε την κάρτα
            st.markdown(f"""
                <div class="match-card">
                    <div class="league-title">🏆 {current_league}</div>
                    <div class="team-names">{teams}</div>
                    <div class="prediction">🎯 {tip}</div>
                </div>
            """, unsafe_allow_html=True)
        elif "Ενημέρωση" in line:
            st.info(f"📅 {line}")
else:
    st.error("Περιμένουμε τα δεδομένα...")
