st.markdown("""
    <style>
    /* Premium Look */
    .stApp { background-color: #0b0f19; color: white; }
    .main-title { 
        font-size: 35px; font-weight: bold; text-align: center; 
        color: #FFD700; /* Χρυσό χρώμα */
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    .sub-title { text-align: center; color: #00d4ff; font-size: 18px; margin-bottom: 25px; font-style: italic; }
    
    .match-card {
        background: linear-gradient(145deg, #161b22, #0d1117);
        border-radius: 15px;
        padding: 18px;
        margin-bottom: 15px;
        border: 1px solid #30363d;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .league-name { color: #FFD700; font-size: 13px; font-weight: bold; }
    .match-time { color: #ffffff; background: #c0392b; padding: 2px 8px; border-radius: 5px; font-size: 11px; }
    .teams { font-size: 18px; font-weight: bold; color: #e6edf3; margin: 12px 0; }
    .prob-text { font-size: 12px; color: #8b949e; }
    </style>
    """, unsafe_allow_html=True)

# Τίτλος με Λογότυπο (Emoji)
st.markdown('<div class="main-title">⚡ MARIOS PRO-BET PRO ⚡</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Advanced Poisson Prediction Engine</div>', unsafe_allow_html=True)
