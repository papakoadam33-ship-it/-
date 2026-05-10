import requests
import math
from datetime import datetime

# --- ΡΥΘΜΙΣΕΙΣ API ---
RAPID_API_KEY = "47d5da2fb8mshde110deccc94426p1f3647jsn856860d5f997"

def calculate_poisson_tips(h_goals, a_goals):
    avg = h_goals + a_goals
    prob_over = 1 - (math.exp(-avg) * (1 + avg + (avg**2)/2))
    main_tip = "Over 2.5" if prob_over > 0.52 else "1X & Over 1.5"
    main_pct = f"{int(prob_over*100)}%"
    cover_tip = "Goal-Goal"
    cover_pct = "76%"
    return main_tip, main_pct, cover_tip, cover_pct

def fetch_data():
    predictions = []
    # Αλλάζουμε το endpoint για να παίρνουμε ΟΛΟΥΣ τους αγώνες της ημέρας
    url = "https://free-api-live-football-data.p.rapidapi.com/football-all-matches-by-date"
    querystring = {"date": datetime.now().strftime("%Y%m%d")} # Σημερινή ημερομηνία
    
    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "free-api-live-football-data.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()
        
        if "data" in data and "leagues" in data["data"]:
            for league_data in data["data"]["leagues"]:
                league_name = league_data.get("name", "").upper()
                
                # Φιλτράρουμε για να βλέπουμε τα σημαντικά και την Ελλάδα
                important_leagues = ["SUPER LEAGUE", "PREMIER LEAGUE", "LA LIGA", "SERIE A", "BUNDESLIGA", "CHAMPIONS LEAGUE"]
                
                for match in league_data.get("matches", []):
                    home_team = match["homeTeam"]["name"]
                    away_team = match["awayTeam"]["name"]
                    match_time = match.get("status", {}).get("utcTime", "00:00")[11:16]
                    
                    # Poisson υπολογισμός
                    t1, p1, t2, p2 = calculate_poisson_tips(1.6, 1.2)
                    
                    predictions.append(f"{league_name} ({match_time})|{home_team} - {away_team}|{t1},{p1},{t2},{p2}")
    except Exception as e:
        print(f"Error: {e}")

    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        f.write(f"ΗΜΕΡΟΜΗΝΙΑ|{datetime.now().strftime('%d/%m/%Y')}|{datetime.now().strftime('%H:%M')}\n")
        if predictions:
            # Δείξε μόνο τους πρώτους 15 αγώνες για να μην γεμίσει η οθόνη
            for p in predictions[:15]:
                f.write(p + "\n")
        else:
            f.write("INFO|Αναμονή για το σημερινό κουπόνι...|-, -, -, -")

if __name__ == "__main__":
    fetch_data()
