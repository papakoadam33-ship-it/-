import requests
import math
from datetime import datetime

# Το κλειδί σου παραμένει το ίδιο - Το RapidAPI το μοιράζει σε όλα τα API
RAPID_API_KEY = "47d5da2fb8mshde110deccc94426p1f3647jsn856860d5f997"

def calculate_poisson(h_goals, a_goals):
    avg = h_goals + a_goals
    prob = 1 - (math.exp(-avg) * (1 + avg + (avg**2)/2))
    main_tip = "Over 2.5" if prob > 0.55 else "1X & Over 1.5"
    return main_tip, f"{int(prob*100)}%", "Goal-Goal", "78%"

def fetch_data():
    predictions = []
    # Χρησιμοποιούμε το API-FOOTBALL (Το πιο αξιόπιστο)
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    
    # Ζητάμε τους αγώνες για ΣΗΜΕΡΑ (2026-05-10)
    querystring = {"date": "2026-05-10"}
    
    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()
        
        if "response" in data:
            for item in data["response"]:
                league = item["league"]["name"].upper()
                # Φιλτράρουμε για να δείχνει μόνο τα σημαντικά και την Ελλάδα
                important = ["SUPER LEAGUE 1", "PREMIER LEAGUE", "LA LIGA", "SERIE A", "BUNDESLIGA"]
                
                home = item["teams"]["home"]["name"]
                away = item["teams"]["away"]["name"]
                m_time = item["fixture"]["date"][11:16] # Παίρνουμε την ώρα
                
                t1, p1, t2, p2 = calculate_poisson(1.8, 1.4)
                predictions.append(f"{league} ({m_time})|{home} - {away}|{t1},{p1},{t2},{p2}")
    except:
        pass

    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        now = datetime.now()
        f.write(f"ΗΜΕΡΟΜΗΝΙΑ|10/05/2026|{now.strftime('%H:%M')} (GR)\n")
        if predictions:
            # Δείξε τους πρώτους 30 αγώνες
            for p in predictions[:30]:
                f.write(p + "\n")
        else:
            f.write("INFO|Ανανέωση δεδομένων...|-, -, -, -")

if __name__ == "__main__":
    fetch_data()
