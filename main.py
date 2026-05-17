import streamlit as st
import os

# Ρύθμιση της σελίδας με το νέο εικονίδιο Μπάλας Ποδοσφαίρου
st.set_page_config(page_title="Marios Pro-Bet Pro", page_icon="https://img.icons8.com/emoji/96/soccer-ball-emoji.png", layout="centered")

# Έξυπνο HTML κόλπο για να εξαναγκάσουμε τα κινητά να δουν τη μπάλα ποδοσφαίρου ως εικονίδιο συντόμευσης
st.markdown("""
    <head>
        <link rel="icon" type="image/png" href="https://img.icons8.com/emoji/96/soccer-ball-emoji.png">
        <link rel="apple-touch-icon" href="https://img.icons8.com/emoji/96/soccer-ball-emoji.png">
    </head>
""", unsafe_allow_html=True)

# Επιβολή μόνιμου Dark Mode και στυλ της εφαρμογής
st.markdown("""
    <style>
    /* Κλείδωμα μαύρου φόντου παντού */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stCanvasBackground"] {
        background-color: #121212 !important;
    }
    
    /* Πανέμορφο μαύρο πλαίσιο για τον τίτλο */
    .custom-header { 
        text-align: center; 
        background-color: #1E1E1E !important; 
        padding: 20px 10px !important; 
        border-radius: 15px !important; 
        border: 1px solid #333333 !important;
        margin-top: 10px !important;
        margin-bottom: 25px !important; 
        box-shadow: 2px 2px 10px rgba(0,0,0,0.5) !important;
    }
    .title-text { color: #FFFFFF !important; font-size: 30px !important; font-weight: 800 !important; margin-bottom: 8px !important; letter-spacing: 1px !important; }
    .model-text { color: #FFD700 !important; font-size: 16px !important; font-weight: bold !important; font-style: italic !important; margin-top: 0px !important; letter-spacing: 0.5px !important; }
    
    /* Διαχωριστικοί Τίτλοι για Κατηγορίες */
    .section-title { color: #FFD700 !important; font-size: 20px !important; font-weight: bold !important; margin: 25px 0 15px 0 !important; border-left: 4px solid #FFD700 !important; padding-left: 10px !important; text-transform: uppercase !important; }
    .section-title-vip { color: #FF4D4D !important; font-size: 22px !important; font-weight: bold !important; margin: 25px 0 15px 0 !important; border-left: 4px solid #FF4D4D !important; padding-left: 10px !important; text-transform: uppercase !important; }

    .time-banner { background-color: #1E1E24 !important; padding: 10px !important; border-radius: 10px !important; border: 2px solid #FFD700 !important; text-align: center !important; color: #FFD700 !important; font-size: 16px !important; font-weight: bold !important; margin-bottom: 25px !important; }
    
    /* Κουτιά Αγώνων */
    .match-box { background-color: #1E1E1E !important; padding: 15px !important; border-radius: 15px !important; border: 1px solid #333333 !important; margin-bottom: 15px !important; box-shadow: 2px 2px 10px rgba(0,0,0,0.5) !important; }
    .match-box-vip { background-color: #221A00 !important; padding: 15px !important; border-radius: 15px !important; border: 2px solid #FFD700 !important; margin-bottom: 15px !important; box-shadow: 0px 0px 15px rgba(255, 215, 0, 0.3) !important; }
    
    .league-title { color: #FFD700 !important; font-size: 13px !important; font-weight: bold !important; text-transform: uppercase !important; letter-spacing: 1px !important; }
    .teams-title { color: #FFFFFF !important; font-size: 22px !important; font-weight: bold !important; margin: 5px 0 !important; }
    .time-badge { background-color: #D9534F !important; color: white !important; padding: 3px 8px !important; border-radius: 5px !important; font-size: 13px !important; font-weight: bold !important; display: inline-block !important; margin-bottom: 10px !important; }
    
    .tip-box { background-color: #5CB85C !important; color: white !important; padding: 12px; border-radius: 8px; text-align: center; font-weight: bold; margin-top: 10px; font-size: 17px; }
    .tip-box-vip { background-color: #D4AF37 !important; color: black !important; padding: 12px; border-radius: 8px; text-align: center; font-weight: 900; margin-top: 10px; font-size: 18px; text-transform: uppercase; box-shadow: 0px 4px 6px rgba(0,0,0,0.2); }
    
    .cover-box { background-color: #E67E22 !important; color: white !important; padding: 12px; border-radius: 8px; text-align: center; font-weight: bold; margin-top: 8px; font-size: 16px; }
    .info-box { background-color: #1E1E1E !important; padding: 20px; border-radius: 15px; border: 1px solid #333333; text-align: center; margin-bottom: 15px; }
    .info-text { color: #FFFFFF !important; font-size: 20px; font-weight: bold; margin: 15px 0; }
    </style>
""", unsafe_allow_html=True)

# Κεφαλίδα της εφαρμογής
st.markdown("""
    <div class="custom-header">
        <div class="title-text">⚡ MARIOS PRO-BET PRO ⚡</div>
        <div class="model-text">Poisson Distribution Model</div>
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
                        
                        if pct >= 65:
                            vip_picks.append(item)
                        else:
                            normal_picks.append(item)
            
            # 1. VIP PICKS
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
            
            # 2. ΥΠΟΛΟΙΠΟΙ ΑΓΩΝΕΣ
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
else:
    st.markdown("<div class='time-banner'>📅 ΠΡΟΓΝΩΣΤΙΚΑ --/--/----</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #555555; font-size: 12px; margin-top: 20px;'>Powered by Python & Football-Data API</p>", unsafe_allow_html=True)
