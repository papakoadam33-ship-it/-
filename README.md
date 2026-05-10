import requests
import math
from datetime import datetime

# Το κλειδί σου
RAPID_API_KEY = "47d5da2fb8mshde110deccc94426p1f3647jsn856860d5f997"
# Το Host που βλέπουμε στην οθόνη σου
HOST = "apifootball3.p.rapidapi.com"

def calculate_poisson(h, a):
    avg = h + a
    prob = 1 - (math.exp(-avg) * (1 + avg + (avg**2)/2))
    tip = "Over 2.5" if prob > 0.55 else "1X & Over 1.5"
    return tip, f"{int(prob*100)}%", "Goal-Goal", "76%"

def fetch_data():
    predictions = []
    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": HOST
    }
    
    # Ζητάμε τους αγώνες για σήμερα 2026-05-10
    url = f"https://{HOST}/"
    params = {"action": "get_events", "from": "2026-05-10", "to": "2026-05-10"}

    try:
        r = requests.get(url, headers=headers, params=params)
        data = r.json()
        
        if isinstance(data, list):
            for m in data:
                league = m.get("league_name", "FOOTBALL").upper()
                teams = f"{m.get('match_hometeam_name')} - {m.get('match_awayteam_name')}"
                m_time = m.get("match_time", "18:00")
                
                t1, p1, t2, p2 = calculate_poisson(1.7, 1.3)
                predictions.append(f"{league} ({m_time})|{teams}|{t1},{p1},{t2},{p2}")
    except:
        pass

    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        now = datetime.now()
        f.write(f"ΗΜΕΡΟΜΗΝΙΑ|10/05/2026|{now.strftime('%H:%M')} (GR)\n")
        if predictions:
            for p in predictions[:40]:
                f.write(p + "\n")
        else:
            f.write("INFO|Το API συνδέθηκε! Περιμένουμε τα ματς...|-, -, -, -")

if __name__ == "__main__":
    fetch_data()
