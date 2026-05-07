import streamlit as st
import os

# Ρύθμιση Εμφάνισης
st.set_page_config(page_title="Marios Pro-Bet", page_icon="⚽", layout="centered")

# Custom CSS για πιο όμορφο look
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stText { font-family: 'monospace'; font-size: 14px; background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #ddd; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚽ Marios Pro-Bet")
st.write("Καλώς ήρθατε στα πιο έξυπνα προγνωστικά βασισμένα σε AI ανάλυση.")
st.markdown("---")

filename = "daily_predictions.txt"

if os.path.exists(filename):
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    
    if content:
        st.subheader("📋 Προγνωστικά Εβδομάδας")
        st.text(content)
        st.success("✅ Τα δεδομένα είναι ενημερωμένα.")
    else:
        st.info("🔄 Γίνεται ανανέωση των δεδομένων... Δοκιμάστε σε λίγα λεπτά.")
else:
    st.error("❌ Το αρχείο δεδομένων δεν βρέθηκε. Παρακαλώ τρέξτε το GitHub Action.")

st.markdown("---")
st.caption("© 2026 Marios Pro-Bet | Data provided by API-Football")
