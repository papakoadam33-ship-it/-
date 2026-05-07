import streamlit as st
import os

st.set_page_config(page_title="Marios Pro-Bet", page_icon="⚽")

st.title("⚽ Marios Pro-Bet")
st.markdown("---")

# Το όνομα του αρχείου που δημιουργεί το GitHub Actions
filename = "daily_predictions.txt"

if os.path.exists(filename):
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
        
    if content:
        # Εμφάνιση του περιεχομένου
        st.text_area("📋 Σημερινά Προγνωστικά", content, height=500)
        st.success("✅ Τα προγνωστικά ενημερώθηκαν επιτυχώς από το GitHub!")
    else:
        st.warning("Το αρχείο είναι άδειο. Περίμενε την επόμενη ενημέρωση.")
else:
    st.error(f"⚠️ Το αρχείο {filename} δεν βρέθηκε. Βεβαιώσου ότι το GitHub Action έχει ολοκληρωθεί τουλάχιστον μία φορά.")

st.markdown("---")
st.caption("Τελευταία αυτόματη ενημέρωση μέσω GitHub Actions")

