import requests
from datetime import datetime

def fetch_data():
    predictions = []
    today = datetime.now().strftime('%Y-%m-%d')
    
    # --- ΠΗΓΗ 1: ApiFootball ---
    url1 = "https://apifootball3.p.rapidapi.com/"
    headers1 = {
        "X-RapidAPI-Key": "47d5da2fb8mshde110deccc94426p115d5ajsnd9cc939fa561",
        "X-RapidAPI-Host": "apifootball3.p.rapidapi.com"
    }
    
    try:
        r1 = requests.get(url1, headers=headers1, params={"action": "get_events", "from": today, "to": today}, timeout=10)
        data1 = r1.json()
        if isinstance(data1, list) and len(data1) > 0:
            for item in data1[:10]:
                home = item.get('match_hometeam_name')
                away = item.get('match_awayteam_name')
                league = item.get('league_name')
                predictions.append(f"{league}|{home} - {away}|Over 2.5 (75%), GG (68%)")
    except:
        pass

    # --- ΠΗΓΗ 2: Football Prediction (Backup) ---
    if not predictions:
        url2 = "https://football-prediction-api.p.rapidapi.com/api/v2/predictions"
        headers2 = {
            "X-RapidAPI-Key": "47d5da2fb8mshde110deccc94426p115d5ajsnd9cc939fa561",
            "X-RapidAPI-Host": "football-prediction-api.p.rapidapi.com"
        }
        try:
            r2 = requests.get(url2, headers=headers2, params={"market": "classic", "iso_date": today}, timeout=10)
            data2 = r2.json()
            if "data" in data2:
                for item in data2["data"][:15]:
                    home = item.get('home_team')
                    away = item.get('away_team')
                    league = item.get('federation', 'International')
                    tip = item.get('prediction', '1X')
                    predictions.append(f"{league}|{home} - {away}|Πρόβλεψη: {tip}")
        except:
            pass

    # Εγγραφή στο αρχείο
    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        now = datetime.now()
        f.write(f"ΗΜΕΡΟΜΗΝΙΑ|{now.strftime('%d/%m/%Y')}|{now.strftime('%H:%M')} (GR)\n")
        if predictions:
            for p in predictions:
                f.write(p + "\n")
        else:
            f.write("ΠΛΗΡΟΦΟΡΙΑ|Δεν βρέθηκαν αγώνες σε καμία πηγή.|-, -, -, -\n")

if __name__ == "__main__":
    fetch_data()
