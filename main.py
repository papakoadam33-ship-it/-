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
    # Δοκιμάζουμε το endpoint για ΟΛΟΥΣ τους αγώνες
    url = "https://free-api-live-football-data.p.rapidapi.com/football-all-matches-by-date"
    querystring = {"date": datetime.now().strftime("%Y%m%d")}
    
    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "free-api-live-football-data.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()
        
        # Έλεγχος αν υπάρχουν δεδομένα
        if "data" in data and "leagues" in data["data"]:
            for league in data["data"]["leagues"]:
                l_name = league.get("name", "Unknown").upper()
                for m in league.get("matches", []):
                    home = m["homeTeam"]["name"]
                    away = m["awayTeam"]["name"]
                    # Παίρνουμε την ώρα (αν υπάρχει)
                    status = m.get("status", {})
                    time = status.get("utcTime", "2026-05-10T15:00:00Z")[11:16]
                    
                    t1, p1, t2, p2 = calculate_poisson_tips(1.7, 1.3)
                    predictions.append(f"{l_name} ({time})|{home} - {away}|{t1},{p1},{t2},{p2}")
        
        # Αν η πρώτη προσπάθεια απέτυχε, δοκιμάζουμε τους LIVE αγώνες
        if not predictions:
            live_url = "https://free-api-live-football-data.p.rapidapi.com/football-current-matches"
            r_live = requests.get(live_url, headers=headers)
            live_data = r_live.json()
            if "data" in live_data and "matches" in live_data["data"]:
                for m in live_data["data"]["matches"]:
                    l_name = m.get("leagueName", "LIVE").upper()
                    home = m["homeTeam"]["name"]
                    away = m["awayTeam"]["name"]
                    t1, p1, t2, p2 = calculate_poisson_tips(1.8, 1.4)
                    predictions.append(f"{l_name} (LIVE)|{home} - {away}|{t1},{p1},{t2},{p2}")

    except Exception as e:
        print(f"Σφάλμα: {e}")

    # Γράψιμο στο αρχείο
    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        f.write(f"ΗΜΕΡΟΜΗΝΙΑ|{datetime.now().strftime('%d/%m/%Y')}|{datetime.now().strftime('%H:%M')}\n")
        if predictions:
            for p in predictions[:25]: # Δείξε μέχρι 25 αγώνες
                f.write(p + "\n")
        else:
            f.write("INFO|Αναμονή για το σημερινό κουπόνι...|-, -, -, -")

if __name__ == "__main__":
    fetch_data()

