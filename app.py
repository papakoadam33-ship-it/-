import streamlit as st

# Ρύθμιση σελίδας
st.set_page_config(page_title="Marios Pro-Bet Pro", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMarkdown h1 { color: #f1c40f; text-align: center; font-size: 38px; text-shadow: 2px 2px #000; font-weight: bold; }
    
    /* ΤΟ ΝΕΟ ΧΡΥΣΟ ΠΛΑΙΣΙΟ ΠΑΝΩ */
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
    }
    .league-title { color: #f1c40f; font-weight: bold; font-size: 18px; }
    .teams-title { color: #ffffff; font-size: 22px; font-weight: bold; margin: 10px 0; }
    .time-badge {
        background-color: #e74c3c;
        color: white;
        padding: 4px 12px;
        border-radius: 6px;
        float: right;
        font-weight: bold;
    }
    .tip-box {
        display: inline-block;
        padding: 10px 18px;
        border-radius: 10px;
        margin-top: 10px;
        font-weight: bold;
    }
    .main-tip { background-color: #27ae60; color: white; margin-right: 10px; }
    .cover-tip { background-color: #d35400; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.write("# ⚡ MARIOS PRO-BET PRO ⚡")

try:
    with open("daily_predictions.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    if lines:
        header = lines[0].strip().split("|")
        # Εφαρμογή του νέου χρυσού πλαισίου
        st.markdown(f"""
        <div class="info-container">
            📅 {header[1]} | 🕒 Τελευταία Ενημέρωση: {header[2]}
        </div>
        """, unsafe_allow_html=True)
        
        for line in lines[1:]:
            parts = line.strip().split("|")
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
except Exception as e:
    st.error("Αναμονή για δεδομένα...")
