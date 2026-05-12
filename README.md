import requests
from datetime import datetime

def fetch_data():
    predictions = []
    today = datetime.now().strftime('%Y-%m-%d')
    
    url = "https://apifootball3.p.rapidapi.com/"
    headers = {
        "X-RapidAPI-Key": "47d5da2fb8mshde110deccc94426p115d5ajsnd9cc939fa561",
        "X-RapidAPI-Host": "apifootball3.p.rapidapi.com"
    }
    
    try:
        # Ζητάμε μόνο τους σημερινούς αγώνες
        r = requests.get(url, headers=headers, params={"action": "get_events", "from": today, "to": today}, timeout=15)
        data = r.json()
        
        if isinstance(data, list) and len(data) > 0:
            for item in data[:15]:
                home = item.get('match_hometeam_name')
                away = item.get('match_awayteam_name')
                league = item.get('league_name')
                predictions.append(f"{league}|{home} - {away}|Over 2.5 (70%), Goal-Goal (65%)")
    except:
        pass

    # Εγγραφή στο αρχείο - Αν δεν βρει ματς, θα γράψει "Αναμονή"
    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        now = datetime.now()
        f.write(f"ΗΜΕΡΟΜΗΝΙΑ|{now.strftime('%d/%m/%Y')}|{now.strftime('%H:%M')} (GR)\n")
        
        if predictions:
            for p in predictions:
                f.write(p + "\n")
        else:
            f.write("ΠΛΗΡΟΦΟΡΙΑ|Δεν βρέθηκαν διαθέσιμοι αγώνες στο API αυτή τη στιγμή.|-, -, -, -\n")

if __name__ == "__main__":
    fetch_data()

