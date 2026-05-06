import streamlit as st
import os

st.set_page_config(page_title="Marios Pro Tips", page_icon="⚽")

st.title("⚽ Marios Betting Tips")

# ΕΔΩ ΕΙΝΑΙ Ο ΕΛΕΓΧΟΣ
if os.path.exists("daily_predictions.txt"):
    with open("daily_predictions.txt", "r", encoding="utf-8") as f:
        content = f.read()
        if content.strip():
            st.text(content)
        else:
            st.warning("Το αρχείο είναι άδειο. Περίμενε την επόμενη ενημέρωση!")
else:
    st.error("Το αρχείο daily_predictions.txt δεν βρέθηκε ακόμα. Τρέξε το Action στο GitHub!")


