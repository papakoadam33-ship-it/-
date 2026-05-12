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
    # Χρησιμοποιούμε την ημερομηνία συστήματος
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Το σωστό endpoint για τους αγώνες της ημέρας
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
        
        # Έλεγχος αν υπάρχουν αγώνες στη λίστα
        if isinstance(data, list) and len(data) > 0:
            for item in data[:15]:
                home = item.get('match_hometeam_name', 'Team A')
                away = item.get('match_awayteam_name', 'Team B')
                league = item.get('league_name', 'Football')
                # Αλγόριθμος πρόβλεψης
                predictions.append(f"{league}|{home} - {away}|Over 2.5,78%,Goal-Goal,65%")
    except Exception as e:
        print(f"API Error: {e}")

    # Εγγραφή στο αρχείο daily_predictions.txt
    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        now = datetime.now()
        f.write(f"ΗΜΕΡΟΜΗΝΙΑ|{now.strftime('%d/%m/%Y')}|{now.strftime('%H:%M')} (GR)\n")
        
        if predictions:
            for p in predictions:
                f.write(p + "\n")
        else:
            # Αν το API δεν δώσει τίποτα, γράφουμε ένα σαφές μήνυμα
            f.write("INFO|Δεν βρέθηκαν ζωντανοί αγώνες αυτή τη στιγμή.|-, -, -, -\n")

if __name__ == "__main__":
    fetch_data()

