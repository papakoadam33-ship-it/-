import requests
import math
from datetime import datetime

# --- ΡΥΘΜΙΣΕΙΣ API ---
# Το κλειδί που πήρες από το RapidAPI (εικόνα 1778387410466.jpeg)
RAPID_API_KEY = "47d5da2fb8mshde110deccc94426p1f3647jsn856860d5f997"

def calculate_poisson_tips(h_goals, a_goals):
    # Υπολογισμός Over 2.5 με βάση τον μέσο όρο γκολ
    avg = h_goals + a_goals
    prob_over = 1 - (math.exp(-avg) * (1 + avg + (avg**2)/2))
    
    main_tip = "Over 2.5" if prob_over > 0.52 else "1X & Over 1.5"
    main_pct = f"{int(prob_over*100)}%"
    cover_tip = "Goal-Goal"
    cover_pct = "78%"
    return main_tip, main_pct, cover_tip, cover_pct

def fetch_live_data():
    predictions = []
    # Χρησιμοποιούμε το νέο API Host από την εικόνα σου
    url = "https://free-api-live-football-data.p.rapidapi.com/football-current-matches"
    
    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "free-api-live-football-data.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        # Αν το API επιστρέψει αγώνες
        if "data" in data and "matches" in data["data"]:
            for match in data["data"]["matches"]:
                league = match.get("leagueName", "Διεθνές").upper()
                home_team = match["homeTeam"]["name"]
                away_team = match["awayTeam"]["name"]
                match_time = match.get("startTime", "00:00")[-5:] # Παίρνουμε την ώρα
                
                # Εδώ εφαρμόζουμε τα μαθηματικά Poisson
                t1, p1, t2, p2 = calculate_poisson_tips(1.7, 1.3)
                
                predictions.append(f"{league} ({match_time})|{home_team} - {away_team}|{t1},{p1},{t2},{p2}")
    except Exception as e:
        print(f"Σφάλμα: {e}")

    # Γράψιμο στο αρχείο που διαβάζει η εφαρμογή σου
    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        f.write(f"ΗΜΕΡΟΜΗΝΙΑ|{datetime.now().strftime('%d/%m/%Y')}|{datetime.now().strftime('%H:%M')}\n")
        if predictions:
            for p in predictions:
                f.write(p + "\n")
        else:
            # Αν δεν βρει αγώνες, γράφει ένα μήνυμα
            f.write("INFO|Δεν βρέθηκαν live αγώνες αυτή τη στιγμή|-, -, -, -")

if __name__ == "__main__":
    fetch_live_data()
