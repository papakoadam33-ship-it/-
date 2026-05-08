import streamlit as st
import os

st.set_page_config(page_title="Marios Pro-Bet", page_icon="⚽")

# CSS για την εμφάνιση
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .match-card {
        background-color: #1f2937;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 12px;
        border-left: 6px solid #10b981;
    }
    .update-box {
        background-color: #262730;
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #3b82f6;
        margin-bottom: 20px;
    }
    .league { color: #3b82f6; font-size: 12px; font-weight: bold; text-transform: uppercase; }
    .teams { font-size: 17px; font-weight: bold; color: white; margin: 5px 0; }
    .tip { color: #10b981; font-weight: bold; background: rgba(16, 185, 129, 0.1); padding: 5px 10px; border-radius: 5px; display: inline-block; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚽ Marios Pro-Bet")

if os.path.exists("daily_predictions.txt"):
    with open("daily_predictions.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    for line in lines:
        line = line.strip()
        if not line: continue
        
        # Εμφάνιση Ημερομηνίας στα Ελληνικά
        if line.startswith("ΗΜΕΡΟΜΗΝΙΑ"):
            parts = line.split("|")
            st.markdown(f"""
                <div class="update-box">
                    <span style="color: #888;">📅 Ημερομηνία:</span> <b>{parts[1]}</b> 
                    <span style="color: #888; margin-left: 10px;">⏰ Ώρα:</span> <b>{parts[2]}</b>
                </div>
            """, unsafe_allow_html=True)
            
        elif "|" in line:
            parts = line.split("|")
            if len(parts) == 3:
                # Μετάφραση Λίγκας αν είναι γνωστή (προαιρετικά)
                league = parts[0].strip().replace("Premier League", "Πρέμιερ Λιγκ").replace("Serie A", "Σέριε Α").replace("Bundesliga", "Μπουντεσλίγκα")
                
                st.markdown(f"""
                    <div class="match-card">
                        <div class="league">🏆 {league}</div>
                        <div class="teams">{parts[1].strip()}</div>
                        <div class="tip">🎯 Πρόβλεψη: {parts[2].strip()}</div>
                    </div>
                """, unsafe_allow_html=True)
else:
    st.info("🔄 Γίνεται λήψη των σημερινών προγνωστικών...")
