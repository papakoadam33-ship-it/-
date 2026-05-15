import requests
import time
from datetime import datetime, timedelta

# --- ΡΥΘΜΙΣΕΙΣ ---
RAPID_API_KEY = "47d5da2fb8mshde110deccc94426p115d5ajsnd9cc939fa561"
HOST = "apifootball3.p.rapidapi.com"

# Εδώ βάζουμε τα ID των πρωταθλημάτων που θέλεις
# 197 = Super League 1 (Ελλάδα), 62 = Ligue 2 (Σεντ Ετιέν), κτλ.
LEAGUES = {
    "197": "SUPER LEAGUE 1",
    "62": "LIGUE 2",
    "152": "PREMIER LEAGUE",
    "302": "LA LIGA",
    "207": "SERIE A",
    "175": "BUNDESLIGA",
    "168": "LIGUE 1"
}

def get_predictions(league_id):
    url = "https://apifootball3.p.rapidapi.com/"
    # Φέρνουμε τους αγώνες για σήμερα (ώρα Ελλάδας)
    now = datetime.utcnow() + timedelta(hours=3)
    today = now.strftime("%Y-%m-%d")
    
    querystring = {
        "action": "get_events",
        "from": today,
        "to": today,
        "league_id": league_id
    }
    
    headers = {
        "x-rapidapi-key": RAPID_API_KEY,
        "x-rapidapi-host": HOST
    }
    
    try:
        response = requests.get(url, headers=headers, params=querystring).json()
        if "error" in response:
            return []
        return response
    except:
        return []

def main():
    all_matches = []
    now_gr = datetime.utcnow() + timedelta(hours=3)
    
    for league_id, league_name in LEAGUES.items():
        matches = get_predictions(league_id)
        
        if isinstance(matches, list):
            for m in matches:
                home = m['match_hometeam_name']
                away = m['match_awayteam_name']
                m_time = m['match_time']
                
                # Δημιουργούμε τυχαίες προβλέψεις (ή μπορούμε να προσθέσουμε Poisson μετά)
                tip = "Over 2.5 (72%)" if int(league_id) % 2 == 0 else "2-3 Goals (55%)"
                cover = "GG (65%)"
                
                all_matches.append(f"{league_name}|{home} - {away}|{m_time}|{tip}|{cover}")
        
        time.sleep(1) # Για να μην μας μπλοκάρει το API

    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        timestamp = now_gr.strftime("%d/%m/%Y %H:%M")
        f.write(f"--- ΠΡΟΓΝΩΣΤΙΚΑ {timestamp} ---\n")
        f.write("ΛΙΓΚΑ|ΑΓΩΝΑΣ|ΩΡΑ|ΠΡΟΒΛΕΨΗ|ΚΑΛΥΨΗ\n")
        
        if not all_matches:
            f.write("INFO|Δεν υπάρχουν αγώνες για σήμερα.|-| - | - \n")
        else:
            for p in all_matches:
                f.write(p + "\n")

if __name__ == "__main__":
    main()

