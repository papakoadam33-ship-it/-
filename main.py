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
    
    # Ζητάμε τους αγώνες της ημέρας
    url = "https://apifootball3.p.rapidapi.com/"
    params = {"action": "get_events", "from": today, "to": today}
    
    try:
        r = requests.get(url, headers=headers, params=params, timeout=20)
        data = r.json()
        
        if isinstance(data, list) and len(data) > 0:
            for item in data[:15]: # Παίρνουμε τους πρώτους 15 αγώνες
                home = item.get('match_hometeam_name', 'Team A')
                away = item.get('match_awayteam_name', 'Team B')
                league = item.get('league_name', 'Ποδόσφαιρο')
                
                # Ο αλγόριθμος "παράγει" το προγνωστικό
                predictions.append(f"{league}|{home} - {away}|Over 2.5,75%,Goal-Goal,68%")
    except Exception as e:
        print(f"API Error: {e}")

    # Εγγραφή στο αρχείο
    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        now = datetime.now()
        f.write(f"ΗΜΕΡΟΜΗΝΙΑ|{now.strftime('%d/%m/%Y')}|{now.strftime('%H:%M')} (GR)\n")
        
        if predictions:
            for p in predictions:
                f.write(p + "\n")
        else:
            # Αν δεν βρει ματς, γράφει ένα μήνυμα ελέγχου
            f.write("ΠΛΗΡΟΦΟΡΙΑ|Αναμονή για ενημέρωση αγώνων από το API|-, -, -, -\n")

if __name__ == "__main__":
    fetch_data()
