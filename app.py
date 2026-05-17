import streamlit as st
import os

st.set_page_config(page_title="Marios Pro-Bet Pro", page_icon="⚡", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #121212; }
    
    .header-container { 
        text-align: center; 
        background-color: #1E1E1E; 
        padding: 20px 10px; 
        border-radius: 15px; 
        border: 1px solid #333333;
        margin-top: 10px;
        margin-bottom: 25px; 
        box-shadow: 2px 2px 10px rgba(0,0,0,0.5);
    }
    .title-text { color: #FFFFFF !important; font-size: 30px !important; font-weight: 800 !important; margin-bottom: 8px !important; letter-spacing: 1px; }
    .model-text { color: #FFD700 !important; font-size: 16px !important; font-weight: bold !important; font-style: italic !important; margin-top: 0px !important; letter-spacing: 0.5px; }
    
    /* Διαχωριστικοί Τίτλοι για Κατηγορίες */
    .section-title { color: #FFD700; font-size: 20px; font-weight: bold; margin: 20px 0 10px 0; border-left: 4px solid #FFD700; padding-left: 10px; text-transform: uppercase; }
    .section-title-vip { color: #FF4D4D; font-size: 22px; font-weight: bold; margin: 20px 0 10px 0; border-left: 4px solid #FF4D4D; padding-left: 10px; text-transform: uppercase; display: flex; align-items: center; }

    .time-banner { background-color: #1E1E24; padding: 10px; border-radius: 10px; border: 2px solid #FFD700; text-align: center; color: #FFD700; font-size: 16px; font-weight: bold; margin-bottom: 25px; }
    
    /* Κουτιά Αγώνων */
    .match-box { background-color: #1E1E1E; padding: 15px; border-radius: 15px; border: 1px solid #333333; margin-bottom: 15px; box-shadow: 2px 2px 10px rgba(0,0,0,0.5); }
    .match-box-vip { background-color: #221A00; padding: 15px; border-radius: 15px; border: 2px solid #FFD700; margin-bottom: 15px; box-shadow: 0px 0px 15px rgba(255, 215, 0, 0.3); }
    
    .league-title { color: #FFD700; font-size: 13px; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; }
    .teams-title { color: #FFFFFF; font-size: 22px; font-weight: bold; margin: 5px 0; }
    .time-badge { background-color: #D9534F; color: white; padding: 3px 8px; border-radius: 5px; font-size: 13px; font-weight: bold; display: inline-block; margin-bottom: 10px; }
    
    .tip-box { background-color: #5CB85C; color: white; padding: 12px; border-radius: 8px; text-align: center; font-weight: bold; margin-top: 10px; font-size: 17px; }
    .tip-box-vip { background-color: #D4AF37; color: black; padding: 12px; border-radius: 8px; text-align: center; font-weight: 900; margin-top: 10px; font-size: 18px; text-transform: uppercase; box-shadow: 0px 4px 6px rgba(0,0,0,0.2); }
    
    .cover-box { background-color: #E67E22; color: white; padding: 12px; border-radius: 8px; text-align: center; font-weight: bold; margin-top: 8px; font-size: 16px; }
    .info-box { background-color: #1E1E1E; padding: 20px; border-radius: 15px; border: 1px solid #333333; text-align: center; margin-bottom: 15px; }
    .info-text { color: #FFFFFF; font-size: 20px; font-weight: bold; margin: 15px 0; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class='header-container'>
        <div class='title-text'>⚡ MARIOS PRO-BET PRO ⚡</div>
        <div class='model-text'>Poisson Distribution Model</div>
    </div>
""", unsafe_allow_html=True)

filename = "daily_predictions.txt"

if os.path.exists(filename):
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    if lines and len(lines) > 1:
        timestamp = lines[0].replace("--- ΠΡΟΓΝΩΣΤΙΚΑ ", "").replace(" ---", "").strip()
        st.markdown(f"<div class='time-banner'>📅 ΠΡΟΓΝΩΣΤΙΚΑ {timestamp}</div>", unsafe_allow_html=True)
        
        match_lines = lines[2:]
        
        if not match_lines or "INFO" in match_lines[0]:
            st.markdown("""
                <div class='info-box'>
                    <span style='font-size: 30px;'>⏰</span>
                    <div class='info-text'>Δεν υπάρχουν προγραμματισμένοι αγώνες για σήμερα.</div>
                    <div style='color: #888888;'>Το σύστημα ανανεώνει τις προβλέψεις αυτόματα.</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            vip_picks = []
            normal_picks = []
            
            for line in match_lines:
                if "|" in line:
                    parts = line.strip().split("|")
                    if len(parts) >= 6:
                        league, match_name, match_time, tip, pct, cover = parts[0], parts[1], parts[2], parts[3], int(parts[4]), parts[5]
                        item = (league, match_name, match_time, tip, pct, cover)
                        
                        # Ξεχωρίζουμε με βάση το ποσοστό (65% και πάνω πάει VIP)
                        if pct >= 65:
                            vip_picks.append(item)
                        else:
                            normal_picks.append(item)
            
            # 1. ΕΜΦΑΝΙΣΗ VIP PICKS (Αν υπάρχουν)
            if vip_picks:
                st.markdown("<div class='section-title-vip'>🔥 VIP PICKS (ΥΨΗΛΟ ΠΟΣΟΣΤΟ >=65%)</div>", unsafe_allow_html=True)
                for league, match_name, match_time, tip, pct, cover in vip_picks:
                    st.markdown(f"""
                        <div class='match-box-vip'>
                            <div class='league-title'>🏆 {league} [VIP]</div>
                            <div class='teams-title'>{match_name}</div>
                            <div class='time-badge'>🕒 {match_time}</div>
                            <div class='tip-box-vip'>👑 {tip} ({pct}%)</div>
                            <div class='cover-box'>🛡️ {cover}</div>
                        </div>
                    """, unsafe_allow_html=True)
            
            # 2. ΕΜΦΑΝΙΣΗ ΥΠΟΛΟΙΠΩΝ ΑΓΩΝΩΝ
            if normal_picks:
                st.markdown("<div class='section-title'>⚽ ΥΠΟΛΟΙΠΟΙ ΣΗΜΕΡΙΝΟΙ ΑΓΩΝΕΣ</div>", unsafe_allow_html=True)
                for league, match_name, match_time, tip, pct, cover in normal_picks:
                    st.markdown(f"""
                        <div class='match-box'>
                            <div class='league-title'>🏆 {league}</div>
                            <div class='teams-title'>{match_name}</div>
                            <div class='time-badge'>🕒 {match_time}</div>
                            <div class='tip-box'>🎯 {tip} ({pct}%)</div>
                            <div class='cover-box'>🛡️ {cover}</div>
                        </div>
                    """, unsafe_allow_html=True)
    else:
        st.markdown("<div class='time-banner'>📅 ΠΡΟΓΝΩΣΤΙΚΑ ΑΝΑΜΟΝΗ</div>", unsafe_allow_html=True)
        st.info("Το αρχείο δεδομένων ανανεώνεται...")
else:
    st.markdown("<div class='time-banner'>📅 ΠΡΟΓΝΩΣΤΙΚΑ --/--/----</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #555555; font-size: 12px; margin-top: 20px;'>Powered by Python & Football-Data API</p>", unsafe_allow_html=True)
