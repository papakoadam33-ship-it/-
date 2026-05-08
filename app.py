import streamlit as st
import os

# 1. Ρυθμίσεις Σελίδας
st.set_page_config(page_title="Marios Pro-Bet", page_icon="⚽", layout="centered")

# 2. Custom CSS για Ελληνική Τυπογραφία και Στυλ
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0e1117 0%, #1a1c24 100%);
        color: white;
    }
    
    .match-card {
        background-color: #262730;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
        border-left: 5px solid #00ff00;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    
    .league-badge {
        background-color: #007bff;
        color: white;
        padding: 3px 12px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: bold;
    }
    
    .teams {
        font-size: 19px;
        font-weight: bold;
        margin: 12px 0;
        color: #ffffff;
    }
    
    .tip-box {
        background-color: rgba(0, 255, 0, 0.1);
        color: #00ff00;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
        border: 1px dashed #00ff00;
        font-size: 16px;
    }
    
    .update-time {
        font-size: 13px;
        color: #aaa;
        text-align: center;
        font-style: italic;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Κεφαλίδα (Header) στα Ελληνικά
st.markdown("<h1 style='text-align: center;'>⚽ Marios Pro-Bet</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>Προγνωστικά Ποδοσφαίρου με Τεχνητή Νοημοσύνη</p>", unsafe_allow_html=True)
st.markdown("---")

# 4. Ανάγνωση και Προβολή Δεδομένων
filename = "daily_predictions.txt"

if os.path.exists(filename):
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Εμφάνιση ώρας τελευταίας ενημέρωσης
    if len(lines) > 1:
        time_text = lines[1].replace("Ενημέρωση:", "Τελευταία Ενημέρωση:").strip()
        st.markdown(f"<p class='update-time'>📅 {time_text}</p>", unsafe_allow_html=True)

    st.write("") # Κενό

    current_league = ""
    for line in lines:
        line = line.strip()
        
        # Εντοπισμός Πρωταθλήματος
        if line.startswith("🏆"):
            current_league = line.replace("🏆", "").strip()
            continue
            
        # Εντοπισμός Αγώνα και Προγνωστικού
        if "⚽" in line or "🔹" in line:
            try:
                # Χωρίζουμε την ομάδα από το προγνωστικό
                parts = line.split("➔")
                teams = parts[0].replace("⚽", "").replace("🔹", "").strip()
                # Μετάφραση του "Προγνωστικό" αν υπάρχει στο κείμενο
                tip = parts[1].replace("Προγνωστικό:", "").strip()
                
                # Δημιουργία Κάρτας
                st.markdown(f"""
                    <div class="match-card">
                        <span class="league-badge">🏆 {current_league}</span>
                        <div class="teams">{teams}</div>
                        <div class="tip-box">🎯 Πρόβλεψη: {tip}</div>
                    </div>
                """, unsafe_allow_html=True)
            except:
                continue
else:
    st.warning("⚠️ Τα προγνωστικά ετοιμάζονται. Παρακαλώ ανανεώστε σε λίγο.")

# 5. Footer
st.markdown("---")
st.caption("© 2026 Marios Pro-Bet | Η ανάλυση βασίζεται σε AI αλγόριθμο")
