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
        "Campeonato Brasileiro Série A": "CAMPEONATO BRASILEIRO SÉRIE A"
    }

    try:
        response = requests.get(url, headers=headers, timeout=20)
        if response.status_code == 429:
            time.sleep(15)
            response = requests.get(url, headers=headers, timeout=20)
            
        data = response.json()

        if "matches" in data:
            for match in data["matches"][:25]:
                eng_league = match['competition']['name']
                league = leagues_info.get(eng_league, eng_league).upper()
                
                home = match['homeTeam']['name']
                away = match['awayTeam']['name']
                
                # Ώρα Ελλάδος
                raw_date = match['utcDate'] 
                dt_obj = datetime.strptime(raw_date, "%Y-%m-%dT%H:%M:%SZ")
                hour = dt_obj.hour + 3
                if hour >= 24: hour -= 24
                match_time = f"{hour:02d}:{dt_obj.minute:02d}"
                
                # Δομή για τη φωτογραφία 1778658582267.jpeg:
                # Πρωτάθλημα | Ομάδες | Ώρα | Κύρια Πρόβλεψη | Κάλυψη
                main_tip = "1X & Over 1.5"
                cover_tip = "Goal-Goal"
                
                predictions.append(f"{league}|{home} - {away}|{match_time}|{main_tip}|{cover_tip}")
        
    except Exception as e:
        print(f"Error: {e}")

    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        now = datetime.now()
        # Ημερομηνία και ώρα για τη χρυσή μπάρα
        f.write(f"ΗΜΕΡΟΜΗΝΙΑ|{now.strftime('%d/%m/%Y')}|{now.strftime('%H:%M')}\n")
        
        if predictions:
            for p in predictions:
                f.write(p + "\n")
        else:
            f.write("INFO|Αναμονή για αγώνες...|--:--|--|--\n")

if __name__ == "__main__":
    fetch_data()

