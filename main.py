import requests
import time
from datetime import datetime

def fetch_data():
    predictions = []
    API_KEY = "a963742bcd5642afbe8c842d057f25ad" 
    url = "https://api.football-data.org/v4/matches"
    headers = { "X-Auth-Token": API_KEY }

    leagues_info = {
        "Premier League": "ΠΡΕΜΙΕΡ ΛΙΓΚ",
        "Championship": "ΤΣΑΜΠΙΟΝΣΙΠ",
        "UEFA Champions League": "ΤΣΑΜΠΙΟΝΣ ΛΙΓΚ",
        "Primera Division": "ΛΑ ΛΙΓΚΑ",
        "Serie A": "ΣΕΡΙΕ Α",
        "Bundesliga": "ΜΠΟΥΝΤΕΣΛΙΓΚΑ",
        "Ligue 1": "ΛΙΓΚ 1",
        "Eredivisie": "ΟΛΛΑΝΔΙΑ",
        "Primeira Liga": "ΠΟΡΤΟΓΑΛΙΑ",
        "Campeonato Brasileiro Série A": "BRAZIL SERIE A"
    }

    try:
        response = requests.get(url, headers=headers, timeout=20)
        if response.status_code == 429:
            time.sleep(15)
            response = requests.get(url, headers=headers, timeout=20)
            
        data = response.json()

        if "matches" in data:
            for match in data["matches"][:20]:
                eng_league = match['competition']['name']
                league = leagues_info.get(eng_league, eng_league).upper()
                home = match['homeTeam']['name']
                away = match['awayTeam']['name']
                
                # Ρύθμιση ώρας (Ελλάδα +3 ώρες από UTC)
                raw_date = match['utcDate'] 
                dt_obj = datetime.strptime(raw_date, "%Y-%m-%dT%H:%M:%SZ")
                hour = dt_obj.hour + 3
                if hour >= 24: hour -= 24
                match_time = f"{hour:02d}:{dt_obj.minute:02d}"
                
                # Αυτή η σειρά δεδομένων είναι ΚΡΙΣΙΜΗ για την εμφάνιση:
                # 1.Πρωτάθλημα | 2.Ομάδες | 3.Ώρα | 4.Κύρια Πρόβλεψη | 5.Κάλυψη
                predictions.append(f"{league}|{home} - {away}|{match_time}|1X & Over 1.5|Goal-Goal")
        
    except Exception as e:
        print(f"Error: {e}")

    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        now = datetime.now()
        # Η πρώτη γραμμή ελέγχει τη χρυσή μπάρα ημερομηνίας
        f.write(f"ΗΜΕΡΟΜΗΝΙΑ|{now.strftime('%d/%m/%Y')}|{now.strftime('%H:%M')}\n")
        
        for p in predictions:
            f.write(p + "\n")

if __name__ == "__main__":
    fetch_data()
