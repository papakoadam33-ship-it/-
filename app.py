import streamlit as st
import os

st.set_page_config(page_title="Marios Pro-Bet", page_icon="⚽")

st.markdown("""
    <style>
    .match-card {
        background-color: #1f2937;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 10px;
        border-left: 6px solid #10b981;
    }
    .league { color: #3b82f6; font-size: 12px; font-weight: bold; }
    .teams { font-size: 16px; font-weight: bold; color: white; margin: 5px 0; }
    .tip { color: #10b981; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚽ Marios Pro-Bet")

if os.path.exists("daily_predictions.txt"):
    with open("daily_predictions.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    for line in lines:
        if "ΕΝΗΜΕΡΩΣΗ" in line:
            st.info(line.strip())
        elif "|" in line:
            parts = line.split("|")
            if len(parts) == 3:
                st.markdown(f"""
                    <div class="match-card">
                        <div class="league">{parts[0].strip()}</div>
                        <div class="teams">{parts[1].strip()}</div>
                        <div class="tip">🎯 {parts[2].strip()}</div>
                    </div>
                """, unsafe_allow_html=True)
else:
    st.write("Ανανέωση...")
