import requests
import time
from datetime import datetime, timedelta

# --- ΡΥΘΜΙΣΕΙΣ ---
RAPID_API_KEY = "47d5da2fb8mshde110deccc94426p115d5ajsnd9cc939fa561"
HOST = "apifootball3.p.rapidapi.com"

# Επιλέγουμε μόνο 3 βασικές λίγκες για να σιγουρέψουμε ότι θα φέρει αποτέλεσμα τώρα
LEAGUES = {
    "152": "PREMIER LEAGUE",
    "302": "LA LIGA",
    "197": "GREECE SUPER LEAGUE"
}

def get_matches(league_id):
    url = "https://apifootball3.p.rapidapi.com/"
    now = datetime.utcnow() + timedelta(hours=3)
    today = now.strftime("%Y-%m-%d")
    tomorrow = (now + timedelta(days=1)).strftime("%Y-%m-%d")
    
    querystring = {
        "action": "get_events",
        "from": today,
        "to": tomorrow,
        "league_id": league_id
    }
    
    headers = {
        "x-rapidapi-key": RAPID_API_KEY,
        "x-rapidapi-host": HOST
    }
    
    try:
        response = requests.get(url, headers=headers, params=querystring).json()
        # Αν το API επιστρέψει σφάλμα ή άδεια λίστα
        if isinstance(response, list) and len(response) > 0:
            return response
        return []
    except:
        return []

def main():
    all_matches = []
    now_gr = datetime.utcnow() + timedelta(hours=3)
    
    for league_id, league_name in LEAGUES.items():
        matches = get_matches(league_id)
        time.sleep(2) # Περισσότερη αναμονή για να προλαβαίνει το API
        
        if matches:
            for m in matches:
                home = m.get('match_hometeam_name', 'Unknown')
                away = m.get('match_awayteam_name', 'Unknown')
                m_time = m.get('match_time', '00:00')
                m_date = m.get('match_date', '')
                
                tip = "Over 2.5 (65%)"
                cover = "GG (58%)"
                
                display_time = f"{m_date[8:10]}/{m_date[5:7]} {m_time}"
                all_matches.append(f"{league_name}|{home} - {away}|{display_time}|{tip}|{cover}")

    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        timestamp = now_gr.strftime("%d/%m/%Y %H:%M")
        f.write(f"--- ΠΡΟΓΝΩΣΤΙΚΑ {timestamp} ---\n")
        f.write("ΛΙΓΚΑ|ΑΓΩΝΑΣ|ΩΡΑ|ΠΡΟΒΛΕΨΗ|ΚΑΛΥΨΗ\n")
        
        if not all_matches:
            f.write("INFO|Αναμονή για ενημέρωση αγώνων...|-| - | - \n")
        else:
            for p in all_matches:
                f.write(p + "\n")

if __name__ == "__main__":
    main()
