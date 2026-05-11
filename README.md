import requests
import math
from datetime import datetime

# Ρυθμίσεις API - ΜΕ ΤΟ ΝΕΟ ΣΟΥ ΚΛΕΙΔΙ
RAPID_API_KEY = "47d5da2fb8mshde110deccc94426p115d5ajsnd9cc939fa561"
HOST = "apifootball3.p.rapidapi.com"

def calculate_poisson(h, a):
    avg = h + a
    prob_over = 1 - (math.exp(-avg) * (1 + avg + (avg**2)/2))
    tip = "Over 2.5" if prob_over > 0.58 else "1X & Over 1.5"
    return tip, f"{int(prob_over*100)}%", "Goal-Goal", "77%"

def fetch_data():
    predictions = []
    headers = {"X-RapidAPI-Key": RAPID_API_KEY, "X-RapidAPI-Host": HOST}
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Χρήση του v3 fixtures που είναι το πιο σταθερό
    url = f"https://{HOST}/v3/fixtures"
    params = {"date": today}

    try:
        r = requests.get(url, headers=headers, params=params)
        data = r.json()
        
        if "response" in data and len(data["response"]) > 0:
            for item in data["response"]:
                league = item["league"]["name"].upper()
                home = item["teams"]["home"]["name"]
                away = item["teams"]["away"]["name"]
                teams = f"{home} - {away}"
                # Παίρνουμε την ώρα από το fixture date
                m_time = item["fixture"]["date"][11:16] 
                
                t1, p1, t2, p2 = calculate_poisson(1.8, 1.4)
                predictions.append(f"{league} ({m_time})|{teams}|{t1},{p1},{t2},{p2}")
        
        if not predictions:
            predictions.append("INFO|Το API συνδέθηκε! Περιμένουμε τους επόμενους αγώνες...|-, -, -, -")

    except Exception as e:
        predictions.append(f"ERROR|Σφάλμα σύνδεσης: {str(e)}|-, -, -, -")

    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        now = datetime.now()
        f.write(f"ΗΜΕΡΟΜΗΝΙΑ|{now.strftime('%d/%m/%Y')}|{now.strftime('%H:%M')} (GR)\n")
        for p in predictions[:50]:
            f.write(p + "\n")

if __name__ == "__main__":
    fetch_data()
