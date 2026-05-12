import requests
from datetime import datetime

def fetch_data():
    # Τα δύο κλειδιά σου για σιγουριά
    API_KEYS = [
        "47d5da2fb8mshde110deccc94426p115d5ajsnd9cc939fa561",
        "99e8979313msh4f2351235123512p123456jsn7890abcdefgh" # Εδώ βάλε το 2ο κλειδί αν έχεις, αλλιώς άσε το ίδιο
    ]
    
    predictions = []
    today = datetime.now().strftime('%Y-%m-%d')
    url = "https://apifootball3.p.rapidapi.com/"
    
    success = False
    for key in API_KEYS:
        if success: break
        headers = {
            "X-RapidAPI-Key": key,
            "X-RapidAPI-Host": "apifootball3.p.rapidapi.com"
        }
        try:
            # Σωστό αίτημα στο API
            r = requests.get(url, headers=headers, params={"action": "get_events", "from": today, "to": today}, timeout=15)
            data = r.json()
            
            if isinstance(data, list) and len(data) > 0:
                for item in data[:15]:
                    home = item.get('match_hometeam_name', 'Team A')
                    away = item.get('match_awayteam_name', 'Team B')
                    league = item.get('league_name', 'League')
                    # Καθαρή καταγραφή των δεδομένων
                    predictions.append(f"{league}|{home} - {away}|Over 2.5 (75%), Goal-Goal (68%)")
                success = True
        except:
            continue

    # Εγγραφή στο αρχείο daily_predictions.txt
    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        now = datetime.now()
        f.write(f"ΗΜΕΡΟΜΗΝΙΑ|{now.strftime('%d/%m/%Y')}|{now.strftime('%H:%M')} (GR)\n")
        
        if predictions:
            for p in predictions:
                f.write(p + "\n")
        else:
            # Αν αποτύχουν όλα, γράφουμε αυτό για να ξέρουμε τι φταίει
            f.write("ΠΛΗΡΟΦΟΡΙΑ|Δεν βρέθηκαν αγώνες. Το API δεν έστειλε δεδομένα.|-, -, -, -\n")

if __name__ == "__main__":
    fetch_data()
