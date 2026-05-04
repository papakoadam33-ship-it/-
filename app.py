import streamlit as st
import os

st.set_page_config(page_title="Prognostika App", page_icon="⚽")

st.title("⚽ Τα Προγνωστικά μου")

# Έλεγχος αν υπάρχει το αρχείο με τα προγνωστικά
if os.path.exists("daily_predictions.txt"):
    with open("daily_predictions.txt", "r", encoding="utf-8") as f:
        content = f.read()
        if content.strip():
            st.text_area("Προβλέψεις Ημέρας", content, height=400)
        else:
            st.warning("Το αρχείο προγνωστικών είναι άδειο.")
else:
    st.error("Δεν βρέθηκαν προγνωστικά. Πρέπει να τρέξεις το GitHub Action πρώτα!")

st.sidebar.info("Τα δεδομένα ανανεώνονται αυτόματα κάθε πρωί μέσω GitHub Actions.")
