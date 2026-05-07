import streamlit as st
import os

# Ρυθμίσεις Σελίδας
st.set_page_config(page_title="Marios Pro-Bet", page_icon="⚽")

# Στυλ για πιο επαγγελματική εμφάνιση
st.markdown("""
    <style>
    .stCode { background-color: #1e1e1e !important; color: #00ff00 !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚽ Marios Pro-Bet")
st.write("AI-Powered Προγνωστικά Ποδοσφαίρου")
st.markdown("---")

filename = "daily_predictions.txt"

if os.path.exists(filename):
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    
    if content.strip():
        st.subheader("📋 Επόμενοι Αγώνες & Tips")
        # Εμφάνιση του περιεχομένου σε πλαίσιο κώδικα για να είναι ευανάγνωστο
        st.code(content, language='text')
        st.success("✅ Τα δεδομένα ενημερώθηκαν επιτυχώς.")
    else:
        st.info("🔄 Τα δεδομένα ανανεώνονται. Παρακαλώ περιμένετε.")
else:
    st.error("❌ Το αρχείο προγνωστικών δεν βρέθηκε. Τρέξτε το GitHub Action.")

st.markdown("---")
st.caption("Powered by Marios AI | 2026")
