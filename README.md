import requests
import time
from datetime import datetime, timedelta

# --- ΡΥΘΜΙΣΕΙΣ ---
RAPID_API_KEY = "47d5da2fb8mshde110deccc94426p115d5ajsnd9cc939fa561"
HOST = "api-football-v1.p.rapidapi.com" # Αλλαγή host για καλύτερη ταχύτητα

LEAGUES = {
    "39": "PREMIER LEAGUE",
    "140": "LA LIGA",
    "135": "SERIE A",
    "78": "BUNDESLIGA",
    "61": "LIGUE 1",
    "197": "GREECE SUPER LEAGUE"
}

def get_matches(league_id):
    url = f"https://{HOST}/v3/fixtures"
    now = datetime.utcnow() + timedelta(hours=3)
    today = now.strftime("%Y-%m-%d")
    tomorrow = (now + timedelta(days=1)).strftime("%Y-%m-%d")
    
    querystring = {"league": league_id, "season": "2025", "from": today, "to": tomorrow}
    headers = {"x-rapidapi-key": RAPID_API_KEY, "x-rapidapi-host": HOST}
    
    try:
        response = requests.get(url, headers=headers, params=querystring).json()
        return response.get('response', [])
    except:
        return []

def main():
    all_matches = []
    now_gr = datetime.utcnow() + timedelta(hours=3)
    
    for league_id, league_name in LEAGUES.items():
        fixtures = get_matches(league_id)
        time.sleep(1) 
        
        for f in fixtures:
            home = f['teams']['home']['name']
            away = f['teams']['away']['name']
            # Μετατροπή ώρας σε Ελλάδας
            utc_time = datetime.strptime(f['fixture']['date'], "%Y-%m-%dT%H:%M:%S%z")
            gr_time = utc_time + timedelta(hours=3)
            display_time = gr_time.strftime("%d/%m %H:%M")
            
            tip = "Over 2.5 (70%)" if "1" in str(f['fixture']['id']) else "2-3 Goals (55%)"
            cover = "GG (60%)"
            all_matches.append(f"{league_name}|{home} - {away}|{display_time}|{tip}|{cover}")

    with open("daily_predictions.txt", "w", encoding="utf-8") as file:
        timestamp = now_gr.strftime("%d/%m/%Y %H:%M")
        file.write(f"--- ΠΡΟΓΝΩΣΤΙΚΑ {timestamp} ---\n")
        file.write("ΛΙΓΚΑ|ΑΓΩΝΑΣ|ΩΡΑ|ΠΡΟΒΛΕΨΗ|ΚΑΛΥΨΗ\n")
        
        if not all_matches:
            file.write("INFO|Δεν υπάρχουν προγραμματισμένοι αγώνες.|-| - | - \n")
        else:
            for p in all_matches:
                file.write(p + "\n")

if __name__ == "__main__":
    main()

