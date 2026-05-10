import requests
import math
from datetime import datetime

RAPID_API_KEY = "47d5da2fb8mshde110deccc94426p1f3647jsn856860d5f997"
HOST = "free-api-live-football-data.p.rapidapi.com"

def calculate_tips(h, a):
    avg = h + a
    prob = 1 - (math.exp(-avg) * (1 + avg + (avg**2)/2))
    return ("Over 2.5", f"{int(prob*100)}%", "Goal-Goal", "75%")

def fetch_data():
    predictions = []
    headers = {"X-RapidAPI-Key": RAPID_API_KEY, "X-RapidAPI-Host": HOST}
    
    # Προσπάθεια 1: Live Αγώνες
    try:
        r = requests.get(f"https://{HOST}/football-current-matches", headers=headers)
        res = r.json()
        matches = res.get("data", {}).get("matches", [])
        for m in matches:
            league = m.get("leagueName", "LIVE").upper()
            teams = f"{m['homeTeam']['name']} - {m['awayTeam']['name']}"
            t1, p1, t2, p2 = calculate_tips(1.8, 1.4)
            predictions.append(f"{league} (LIVE)|{teams}|{t1},{p1},{t2},{p2}")
    except: pass

    # Προσπάθεια 2: Αν δεν βρήκε live, φέρε τους επόμενους σημαντικούς
    if not predictions:
        try:
            # Δοκιμάζουμε να πάρουμε το πρόγραμμα της ημέρας
            r = requests.get(f"https://{HOST}/football-all-matches-by-date", headers=headers, params={"date": datetime.now().strftime("%Y%m%d")})
            res = r.json()
            leagues = res.get("data", {}).get("leagues", [])
            for leg in leagues:
                l_name = leg.get("name", "").upper()
                for m in leg.get("matches", []):
                    teams = f"{m['homeTeam']['name']} - {m['awayTeam']['name']}"
                    t1, p1, t2, p2 = calculate_tips(1.6, 1.2)
                    predictions.append(f"{l_name}|{teams}|{t1},{p1},{t2},{p2}")
        except: pass

    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        f.write(f"ΗΜΕΡΟΜΗΝΙΑ|{datetime.now().strftime('%d/%m/%Y')}|{datetime.now().strftime('%H:%M')}\n")
        if predictions:
            for p in predictions[:30]: f.write(p + "\n")
        else:
            f.write("INFO|Το API δεν έστειλε αγώνες. Δοκίμασε σε λίγο.|-, -, -, -")

if __name__ == "__main__":
    fetch_data()
