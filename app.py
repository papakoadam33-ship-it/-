import streamlit as st
import os

st.set_page_config(page_title="Marios Pro-Bet", page_icon="⚽")

# Τίτλος στα Ελληνικά
st.markdown("<h1 style='text-align: center;'>⚽ Marios Pro-Bet</h1>", unsafe_allow_html=True)
st.markdown("---")

filename = "daily_predictions.txt"

if os.path.exists(filename):
    with open(filename, "r", encoding="utf-8") as f:
        # Διαβάζουμε ΟΛΟ το περιεχόμενο του αρχείου
        content = f.read()
    
    if content.strip():
        # Εμφάνιση όλου του κειμένου όπως είναι
        st.text(content)
    else:
        st.write("🔄 Τα δεδομένα ανανεώνονται...")
else:
    st.error("❌ Το αρχείο δεν βρέθηκε!")
