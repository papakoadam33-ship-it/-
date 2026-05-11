
import streamlit as st
import os

# --- ΡΥΘΜΙΣΗ ΣΕΛΙΔΑΣ ---
st.set_page_config(page_title="Marios Pro-Bet Pro", layout="centered")

# Καθαρισμός μνήμης
st.cache_data.clear()

def load_predictions():
    file_path = 'daily_predictions.txt'
    if not os.path.exists(file_path):
        return [["INFO", "Περιμένουμε το GitHub Action...", "-", "-", "-", "-"]]
    
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        if lines:
            header = lines[0].strip().split('|')
            st.sidebar.info(f"📅 {header[1]} | 🕒 {header[2]}")
            
            for line in lines[1:]:
                parts = line.strip().split('|')
                if len(parts) >= 3:
                    league = parts[0]
                    teams = parts[1]
                    tips = parts[2].split(',')
                    if len(tips) == 4:
                        data.append([league, teams, tips[0], tips[1], tips[2], tips[3]])
    return data

# --- ΕΜΦΑΝΙΣΗ ---
st.markdown("<h1 style='text-align: center;'>⚡ MARIOS PRO-BET PRO ⚡</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-style: italic;'>Advanced Poisson Prediction Engine</p>", unsafe_allow_html=True)

preds = load_predictions()

if not preds:
    st.warning("Αναμονή για ενημέρωση δεδομένων...")
else:
    for p in preds:
        with st.container():
            st.markdown(f"""
            <div style="background-color: #1e2130; padding: 20px; border-radius: 15px; margin-bottom: 20px; border-left: 5px solid #f1c40f; color: white;">
                <p style="color: #f1c40f; font-weight: bold; margin-bottom: 5px;">🏆 {p[0]}</p>
                <h3 style="margin: 0; color: white;">{p[1]}</h3>
                <hr style="border: 0.5px solid #34495e;">
                <div style="display: flex; justify-content: space-between;">
                    <div style="color: #e74c3c; font-weight: bold;">🎯 {p[2]} ({p[3]})</div>
                    <div style="color: #95a5a6;">🛡️ {p[4]} ({p[5]})</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
