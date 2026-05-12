import streamlit as st
import os

# Ρύθμιση σελίδας
st.set_page_config(page_title="Marios Pro-Bet Pro", layout="centered")

def load_predictions():
    file_path = "daily_predictions.txt"
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.readlines()
    return []

st.title("⚡ MARIOS PRO-BET PRO ⚡")
st.write("Advanced Poisson Prediction Engine")

data = load_predictions()

if data:
    # Η πρώτη γραμμή έχει την ημερομηνία
    header = data[0].split("|")
    st.info(f"Τελευταία Ενημέρωση: {header[1]} στις {header[2]}")
    
    # Οι υπόλοιπες γραμμές είναι οι αγώνες
    for line in data[1:]:
        parts = line.split("|")
        if len(parts) >= 3:
            league, teams, tips = parts[0], parts[1], parts[2]
            with st.container():
                st.markdown(f"### 🏆 {league}")
                st.subheader(teams)
                st.write(f"🎯 **Πρόβλεψη:** {tips}")
                st.divider()
else:
    st.warning("⚠️ Τα δωρεάν όρια εξαντλήθηκαν. Εμφάνιση Demo.")

