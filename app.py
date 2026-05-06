import streamlit as st
import os

# Ρυθμίσεις σελίδας για να φαίνεται ωραίο στο κινητό
st.set_page_config(
    page_title="Marios Pro Tips",
    page_icon="⚽",
    layout="centered"
)

# Στυλ για να μοιάζει με πραγματική εφαρμογή
st.markdown("""
    <style>
    .main { background-color: #121212; }
    .league-header {
        background-color: #1e1e1e;
        color: #00ff41;
        padding: 10px;
        border-radius: 5px;
        margin-top: 20px;
        font-weight: bold;
        border-left: 5px solid #00ff41;
    }
    .match-card {
        background-color: #ffffff;
        color: #000000;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0px;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
    }
    .prediction {
        color: #d32f2f;
        font-weight: bold;
        float: right;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("⚽ Marios Pro-Bet Predictions")
st.write("Καθημερινή ενημέρωση από τα κορυφαία πρωταθλήματα")

file_path = "daily_predictions.txt"

if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    if len(lines) > 2:
        for line in lines:
            line = line.strip()
            if not line: continue
            
            # Αν η γραμμή είναι πρωτάθλημα (ξεκινά με ---)
            if line.startswith("---"):
                league_name = line.replace("---", "").strip()
                st.markdown(f'<div class="league-header">{league_name}</div>', unsafe_allow_html=True)
            
            # Αν η γραμμή είναι αγώνας (περιέχει vs)
            elif "vs" in line:
                # Χωρίζουμε το προγνωστικό από το ματς για ωραίο εφέ
                parts = line.split("->")
                match_info = parts[0].strip()
                prediction = parts[1].strip() if len(parts) > 1 else "Over 1.5"
                
                st.markdown(f"""
                    <div class="match-card">
                        {match_info}
                        <span class="prediction">{prediction}</span>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.info("⏳ Αναμονή για τους σημερινούς αγώνες...")
else:
    st.error("❌ Το αρχείο δεδομένων δεν έχει δημιουργηθεί ακόμα. Τρέξε το GitHub Action!")

st.sidebar.markdown("### Σχετικά")
st.sidebar.info("Η εφαρμογή ανανεώνεται αυτόματα κάθε πρωί στις 08:00.")
