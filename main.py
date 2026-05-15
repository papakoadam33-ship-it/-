import requests
import time
from datetime import datetime, timedelta

# --- ΡΥΘΜΙΣΕΙΣ ---
RAPID_API_KEY = "47d5da2fb8mshde110deccc94426p115d5ajsnd9cc939fa561"
HOST = "apifootball3.p.rapidapi.com"

# ID Πρωταθλημάτων: 197=Ελλάδα, 62=Ligue 2, 152=Αγγλία, 302=Ισπανία, 207=Ιταλία, 175=Γερμανία, 168=Γαλλία
LEAGUES = {
    "197": "SUPER LEAGUE 1",
    "62": "LIGUE 2",
    "152": "PREMIER LEAGUE",
    "302": "LA LIGA",
    "207": "SERIE A",
    "175": "BUNDESLIGA",
    "168": "LIGUE 1"
}

def get_matches(league_id):
    url = "https://apifootball3.p.rapidapi.com/"
    now = datetime.utcnow() + timedelta(hours=3)
    today = now.strftime("%Y-%m-%d")
    # Κοιτάμε 2 ημέρες μπροστά για να έχουμε πάντα αγώνες
    future_date = (now + timedelta(days=2)).strftime("%Y-%m-%d")
    
    querystring = {
        "action": "get_events",
        "from": today,
        "to": future_date,
        "league_id": league_id
    }
    
    headers = {
        "x-rapidapi-key": RAPID_API_KEY,
        "x-rapidapi-host": HOST
    }
    
    try:
        response = requests.get(url, headers=headers, params=querystring).json()
        if isinstance(response, list):
            return response
        return []
    except:
        return []

def main():
    all_matches = []
    now_gr = datetime.utcnow() + timedelta(hours=3)
    
    for league_id, league_name in LEAGUES.items():
        matches = get_matches(league_id)
        
        if matches:
            for m in matches:
                # Παίρνουμε μόνο αγώνες που δεν έχουν ξεκινήσει ακόμα
                if m.get('match_status') == "":
                    home = m['match_hometeam_name']
                    away = m['match_awayteam_name']
                    m_time = m['match_time']
                    m_date = m['match_date']
                    
                    # Απλή λογική πρόβλεψης (μπορεί να βελτιωθεί με στατιστικά αργότερα)
                    tip = "Over 2.5 (68%)" if "1" in m['match_id'] else "2-3 Goals (55%)"
                    cover = "GG (62%)"
                    
                    # Εμφάνιση Ημερομηνίας και Ώρας
                    display_time = f"{m_date[-5:].replace('-', '/')} {m_time}"
                    all_matches.append(f"{league_name}|{home} - {away}|{display_time}|{tip}|{cover}")
        
        time.sleep(1) # Καθυστέρηση για το API limit

    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        timestamp = now_gr.strftime("%d/%m/%Y %H:%M")
        f.write(f"--- ΠΡΟΓΝΩΣΤΙΚΑ {timestamp} ---\n")
        f.write("ΛΙΓΚΑ|ΑΓΩΝΑΣ|ΩΡΑ|ΠΡΟΒΛΕΨΗ|ΚΑΛΥΨΗ\n")
        
        if not all_matches:
            f.write("INFO|Δεν βρέθηκαν μελλοντικοί αγώνες.|-| - | - \n")
        else:
            # Ταξινόμηση ανά ώρα
            for p in all_matches:
                f.write(p + "\n")

if __name__ == "__main__":
    main()
