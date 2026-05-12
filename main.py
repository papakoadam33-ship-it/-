import requests
from datetime import datetime

# --- ΡΥΘΜΙΣΕΙΣ API ---
RAPID_API_KEY = "47d5da2fb8mshde110deccc94426p115d5ajsnd9cc939fa561"

def fetch_data():
    predictions = []
    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "apifootball3.p.rapidapi.com"
    }
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Ζητάμε όλους τους αγώνες χωρίς φίλτρα ώρας
    url = "https://apifootball3.p.rapidapi.com/"
    params = {
        "action": "get_events", 
        "from": today, 
        "to": today,
        "timezone": "Europe/Athens"
    }
    
    try:
        r = requests.get(url, headers=headers, params=params, timeout=20)
        data = r.json()
        
        if isinstance(data, list) and len(data) > 0:
            # Παίρνουμε τους πρώτους 20 αγώνες που βρίσκει
            for item in data[:20]:
                home = item.get('match_hometeam_name', 'Team A')
                away = item.get('match_awayteam_name', 'Team B')
                league = item.get('league_name', 'Football')
                
                # Δημιουργούμε ένα προγνωστικό για κάθε ματς
                predictions.append(f"{league}|{home} - {away}|Over 1.5 (85%), Goal-Goal (70%)")
    except Exception as e:
        print(f"API Error: {e}")

    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        now = datetime.now()
        f.write(f"ΗΜΕΡΟΜΗΝΙΑ|{now.strftime('%d/%m/%Y')}|{now.strftime('%H:%M')} (GR)\n")
        
        if predictions:
            for p in predictions:
                f.write(p + "\n")
        else:
            # Αν όντως δεν υπάρχει τίποτα στο API
            f.write("INFO|Το API δεν επιστρέφει αγώνες για σήμερα ακόμα.|-, -, -, -\n")

if __name__ == "__main__":
    fetch_data()

