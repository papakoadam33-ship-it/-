import streamlit as st
import os
from datetime import datetime

# Ρύθμιση σελίδας
st.set_page_config(page_title="Marios Pro-Bet Pro", page_icon="⚡")

# --- CSS ΓΙΑ PREMIUM DESIGN ---
st.markdown("""
    <style>
    /* Φόντο εφαρμογής */
    .stApp { 
        background-color: #0b0f19; 
        color: #e6edf3; 
    }
    
    /* Τίτλος */
    .main-title { 
        font-size: 32px; 
        font-weight: bold; 
        text-align: center; 
        color: #FFD700; /* Gold */
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        margin-top: -20px;
    }
    
    /* Υπότιτλος */
    .sub-title { 
        text-align: center; 
        color: #00d4ff; 
        font-size: 16px; 
        margin-bottom: 25px; 
        font-style: italic; 
    }
    
    /* Κάρτα Αγώνα */
    .match-card {
        background: linear-gradient(145deg, #161b22, #0d1117);
        border-radius: 15px;
        padding: 18px;
        margin-bottom: 15px;
        border: 1px solid #30363d;
        box-shadow: 0 4px 10px rgba(0,0,0,0.4);
    }
    
    .league-row { 
        display: flex; 
        justify-content: space-between; 
        align-items: center; 
    }
    
    .league-name { 
        color: #FFD700; 
        font-size: 12px; 
        font-weight: bold; 
        text-transform: uppercase; 
    }
    
    .match-time { 
        color: #ffffff; 
        background: #c0392b; 
        padding: 2px 8px; 
        border-radius: 5px; 
        font-size: 11px; 
        font-weight: bold;
    }
    
    .teams { 
        font-size: 18px; 
        font-weight: bold; 
        color: #ffffff; 
        margin: 12px 0; 
    }
    
    /* Πλαίσιο Πιθανοτήτων */
    .tip-box { 
        background: rgba(255,255,255,0.03); 
        padding: 12px; 
        border-radius: 10px; 
        border: 1px solid rgba(255,255,255,0.05);
    }
    
    .prob-label { 
        font-size: 11px; 
        color: #8b949e; 
        margin-bottom: 2px; 
    }
    
    .prediction { 
        font-weight: bold; 
        font-size: 15px; 
    }
    
    /* Ενημέρωση */
    .update-box { 
        background-color: #161b22; 
        padding: 10px; 
        border-radius: 10px; 
        text-align: center; 
        border: 1px solid #FFD700; 
        margin-bottom: 20px; 
        font-size: 13px;
        color: #FFD700;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ΕΜΦΑΝΙΣΗ ΤΙΤΛΟΥ ---
st.markdown('<div class="main-title">⚡ MARIOS PRO-BET PRO ⚡</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Advanced Poisson Prediction Engine</div>', unsafe_allow_html=True)

# --- ΑΝΑΓΝΩΣΗ ΔΕΔΟΜΕΝΩΝ ---
if os.path.exists("daily_predictions.txt"):
    with open("daily_predictions.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    for line in lines:
        line = line.strip()
        if not line or "|" not in line: continue
        
        parts = line.split("|")
        
        # Γραμμή Ημερομηνίας
        if line.startswith("ΗΜΕΡΟΜΗΝΙΑ"):
            st.markdown(f'<div class="update-box">📅 {parts[1]} | 🕒 Τελευταία Ενημέρωση: {parts[2]}</div>', unsafe_allow_html=True)
            continue
            
        # Γραμμή Αγώνα
        if len(parts) == 3:
            league_info = parts[0]
            display_time = ""
            if "(" in league_info:
                display_time = league_info[league_info.find("(")+1:league_info.find(")")]
                league_info = league_info.split("(")[0].strip()
            
            # Μετάφραση Λιγκών
            league_fixed = league_info.replace("Premier League", "ΠΡΕΜΙΕΡ ΛΙΓΚ").replace("Serie A", "ΣΕΡΙΕ Α").replace("La Liga", "ΛΑ ΛΙΓΚΑ").replace("Bundesliga", "ΜΠΟΥΝΤΕΣΛΙΓΚΑ")
            
            # Δεδομένα Tips
            tips = parts[2].split(",")
            if len(tips) >= 4:
                t1, p1, t2, p2 = tips[0], tips[1], tips[2], tips[3]

                st.markdown(f"""
                    <div class="match-card">
                        <div class="league-row">
                            <div class="league-name">🏆 {league_fixed}</div>
                            <div class="match-time">🕒 {display_time}</div>
                        </div>
                        <div class="teams">{parts[1]}</div>
                        <div class="tip-box">
                            <div style="display: flex; justify-content: space-between;">
                                <div>
                                    <div class="prob-label">🎯 Κύρια Πρόβλεψη ({p1})</div>
                                    <div class="prediction" style="color: #00ff88;">{t1}</div>
                                </div>
                                <div style="text-align: right;">
                                    <div class="prob-label">🛡️ Κάλυψη ({p2})</div>
                                    <div class="prediction" style="color: #ffaa00;">{t2}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
else:
    st.info("Αναμονή για νέα δεδομένα από τον αλγόριθμο Poisson...")
