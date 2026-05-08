import streamlit as st
import os

st.set_page_config(page_title="Marios Pro-Bet", page_icon="⚽")

# CSS για τέλεια εμφάνιση και μικρότερο τίτλο
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .main-title { font-size: 28px; font-weight: bold; text-align: center; margin-bottom: 20px; color: #ffffff; }
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
    .league { color: #3b82f6; font-size: 13px; font-weight: bold; text-transform: uppercase; }
    .teams { font-size: 16px; font-weight: bold; color: white; margin: 5px 0; }
    .tip { color: #10b981; font-weight: bold; background: rgba(16, 185, 129, 0.1); padding: 5px 10px; border-radius: 5px; display: inline-block; margin-top: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">⚽ Marios Pro-Bet</div>', unsafe_allow_html=True)

if os.path.exists("daily_predictions.txt"):
    with open("daily_predictions.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    for line in lines:
        line = line.strip()
        if not line: continue
        
        if line.startswith("ΗΜΕΡΟΜΗΝΙΑ"):
            parts = line.split("|")
            st.markdown(f"""
                <div class="update-box">
                    <span style="color: #888;">📅</span> <b>{parts[1]}</b> 
                    <span style="color: #888; margin-left: 10px;">⏰</span> <b>{parts[2]}</b>
                </div>
            """, unsafe_allow_html=True)
            
        elif "|" in line:
            parts = line.split("|")
            if len(parts) == 3:
                # Μετάφραση Λίγκας
                league_name = parts[0].strip()
                league_name = league_name.replace("Premier League", "ΠΡΕΜΙΕΡ ΛΙΓΚ")
                league_name = league_name.replace("Serie A", "ΣΕΡΙΕ Α")
                league_name = league_name.replace("Bundesliga", "ΜΠΟΥΝΤΕΣΛΙΓΚΑ")
                league_name = league_name.replace("Ligue 1", "ΛΙΓΚ 1")
                league_name = league_name.replace("Primera Division", "ΛΑ ΛΙΓΚΑ")
                league_name = league_name.replace("Copa Libertadores", "ΚΟΠΑ ΛΙΜΠΕΡΤΑΔΟΡΕΣ")
                
                st.markdown(f"""
                    <div class="match-card">
                        <div class="league">🏆 {league_name}</div>
                        <div class="teams">{parts[1].strip()}</div>
                        <div class="tip">🎯 Πρόβλεψη: {parts[2].strip()}</div>
                    </div>
                """, unsafe_allow_html=True)
else:
    st.info("🔄 Γίνεται λήψη των σημερινών προγνωστικών...")
