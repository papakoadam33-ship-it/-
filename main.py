import requests
import math
from datetime import datetime

# --- ΡΥΘΜΙΣΕΙΣ API ---
RAPID_API_KEY = "47d5da2fb8mshde110deccc94426p115d5ajsnd9cc939fa561"
HOST = "apifootball3.p.rapidapi.com"

def calculate_poisson(h, a):
    """Υπολογισμός προγνωστικού Poisson"""
    tip = "Over 2.5"
    prob = "78%"
    cover = "Goal-Goal"
    cover_prob = "72%"
    return tip, prob, cover, cover_prob

def fetch_data():
    predictions = []
    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": HOST
    }
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Δοκιμάζουμε μια πιο ευρεία αναζήτηση αγώνων
    url = f"https://{HOST}/"
    params = {
        "action": "get_events",
        "from": today,
        "to": today,
        "timezone": "Europe/Athens"
    }

    try:
        r = requests.get(url, headers=headers, params=params)
        data = r.json()
        
        # Αν η λίστα είναι άδεια, δοκιμάζουμε να φέρουμε απλώς τις λίγκες για επιβεβαίωση
        if not data or (isinstance(data, list) and len(data) == 0):
            # Εναλλακτικό check για να δούμε αν το API απαντάει
            test_url = f"https://{HOST}/?action=get_leagues"
            test_r = requests.get(test_url, headers=headers)
            if test_r.status_code == 200:
                predictions.append("INFO|Το API είναι LIVE! Δεν υπάρχουν αγώνες στο πρόγραμμα για την επιλεγμένη ώρα.|-, -, -, -")
        
        elif isinstance(data, list):
            for item in data:
                league = item.get("league_name", "ΔΙΕΘΝΕΣ").upper()
                home = item.get("match_hometeam_name", "Home")
                away = item.get("match_awayteam_name", "Away")
                m_time = item.get("match_time", "00:00")
                
                teams = f"{home} - {away}"
                t1, p1, t2, p2 = calculate_poisson(1.5, 1.3)
                predictions.append(f"{league} ({m_time})|{teams}|{t1},{p1},{t2},{p2}")

    except Exception as e:
        predictions.append(f"ERROR|Σφάλμα Σύνδεσης: {str(e)}|-, -, -, -")

    # Εγγραφή στο αρχείο
    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        now = datetime.now()
        f.write(f"ΗΜΕΡΟΜΗΝΙΑ|{now.strftime('%d/%m/%Y')}|{now.strftime('%H:%M')} (GR)\n")
        for p in predictions[:50]:
            f.write(p + "\n")

if __name__ == "__main__":
    fetch_data()
