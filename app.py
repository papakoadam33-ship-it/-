import streamlit as st
import os

# Ρυθμίσεις εμφάνισης
st.set_page_config(page_title="Marios Pro Tips", page_icon="⚽")

# CSS για ωραίες κάρτες
st.markdown("""
    <style>
    .league-title { color: #2e7d32; font-size: 24px; font-weight: bold; margin-top: 20px; }
    .match-card { 
        background-color: #f9f9f9; 
        padding: 15px; 
        border-radius: 10px; 
        border-left: 5px solid #2e7d32;
        margin-bottom: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
        color: black;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("⚽ Marios Pro-Bet")

# Έλεγχος αν υπάρχει το αρχείο
if os.path.exists("daily_predictions.txt"):
    with open("daily_predictions.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    if len(lines) > 0:
        for line in lines:
            line = line.strip()
            if line.startswith("---"):
                st.markdown(f'<div class="league-title">{line.replace("---", "")}</div>', unsafe_allow_html=True)
            elif "vs" in line:
                st.markdown(f'<div class="match-card">{line}</div>', unsafe_allow_html=True)
    else:
        st.info("⏳ Η λίστα είναι κενή. Ανανέωση σε λίγο...")
else:
    st.error("❌ Το αρχείο daily_predictions.txt δεν βρέθηκε. Τρέξε το GitHub Action!")



