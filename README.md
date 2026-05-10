import requests
import math
import os
from datetime import datetime

# --- ΡΥΘΜΙΣΕΙΣ API (ΜΟΝΟ ΤΟ ΝΕΟ ΚΛΕΙΔΙ) ---
RAPID_API_KEY = "47d5da2fb8mshde110deccc94426p1f3647jsn856860d5f997"
HOST = "free-api-live-football-data.p.rapidapi.com"

def calculate_poisson_tips(h_goals, a_goals):
    # Μαθηματικά Poisson για Over 2.5
    avg = h_goals + a_goals
    prob_over = 1 - (math.exp(-avg) * (1 + avg + (avg**2)/2))
    
    # Επιλογή σημείου
    if prob_over > 0.55:
        main_tip = "Over 2.5"
    else:
        main_tip = "1X & Over 1.5"
    
    main_pct = f"{int(prob_over*100)}%"
    cover_tip = "Goal-Goal"
    cover_pct = "76%"
    return main_tip, main_pct, cover_tip, cover_pct

def fetch_data():
    predictions = []
    # Παίρνουμε ΟΛΟΥΣ τους αγώνες της ημέρας από το ΝΕΟ API
    url = f"https://{HOST}/football-all-matches-by-date"
    querystring = {"date": datetime.now().strftime("%Y%m%d")}
    
    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": HOST
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()
        
        # Καθαρίζουμε και οργανώνουμε τα δεδομένα
        if "data" in data and "leagues" in data["data"]:
            for league_data in data["data"]["leagues"]:
                league_name = league_data.get("name", "").upper()
                
                for match in league_data.get("matches", []):
                    home_team = match["homeTeam"]["name"]
                    away_team = match["awayTeam"]["name"]
                    # Μετατροπή ώρας από το API
                    match_time = match.get("status", {}).get("utcTime", "2026-05-10T15:00:00Z")[11:16]
                    
                    # Poisson Υπολογισμός (εδώ το σύστημα βάζει μέσους όρους γκολ)
                    t1, p1, t2, p2 = calculate_poisson_tips(1.7, 1.2)
                    
                    predictions.append(f"{league_name} ({match_time})|{home_team} - {away_team}|{t1},{p1},{t2},{p2}")
    except Exception as e:
        print(f"Σφάλμα σύνδεσης: {e}")

    # ΔΗΜΙΟΥΡΓΙΑ ΦΡΕΣΚΟΥ ΑΡΧΕΙΟΥ (Διαγράφει τα παλιά)
    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        f.write(f"ΗΜΕΡΟΜΗΝΙΑ|{datetime.now().strftime('%d/%m/%Y')}|{datetime.now().strftime('%H:%M')}\n")
        if predictions:
            # Κρατάμε τους 20 πιο σημαντικούς αγώνες
            for p in predictions[:20]:
                f.write(p + "\n")
        else:
            f.write("INFO|Αναμονή για το σημερινό κουπόνι...|-, -, -, -")

if __name__ == "__main__":
    fetch_data()
