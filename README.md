import requests
from datetime import datetime

# --- ΡΥΘΜΙΣΕΙΣ API ---
RAPID_API_KEY = "47d5da2fb8mshde110deccc94426p115d5ajsnd9cc939fa561"

def fetch_data():
    predictions = []
    headers = {"X-RapidAPI-Key": RAPID_API_KEY}
    today = datetime.now().strftime('%Y-%m-%d')

    # --- ΠΗΓΗ 1: ApiFootball (Σήμανση: AF) ---
    try:
        url1 = "https://apifootball3.p.rapidapi.com/"
        params1 = {"action": "get_events", "from": today, "to": today, "timezone": "Europe/Athens"}
        r1 = requests.get(url1, headers=headers, params=params1)
        data1 = r1.json()
        if isinstance(data1, list) and len(data1) > 0:
            for item in data1[:15]:
                # Προσθέτουμε το [AF] στην αρχή της λίγκας
                league = f"[AF] {item.get('league_name', 'LEAGUE').upper()}"
                teams = f"{item.get('match_hometeam_name')} - {item.get('match_awayteam_name')}"
                predictions.append(f"{league}|{teams}|Over 2.5,75%,Goal-Goal,70%")
    except:
        pass

    # --- ΠΗΓΗ 2: Football Prediction (Σήμανση: FP) ---
    if len(predictions) < 10:
        try:
            url2 = "https://football-prediction-api.p.rapidapi.com/api/v2/predictions"
            params2 = {"market": "classic", "iso_date": today}
            r2 = requests.get(url2, headers=headers, params=params2)
            data2 = r2.json()
            if "data" in data2:
                for item in data2["data"][:15]:
                    teams = f"{item.get('home_team')} - {item.get('away_team')}"
                    # Προσθέτουμε το [FP] στην αρχή της λίγκας
                    league = f"[FP] {item.get('federation', 'INTL').upper()}"
                    tip = item.get("prediction", "1X")
                    prob = item.get("probabilities", {}).get(tip, "80%")
                    if isinstance(prob, (int, float)): prob = f"{int(prob)}%"
                    
                    predictions.append(f"{league}|{teams}|{tip},{prob},Over 1.5,85%")
        except:
            pass

    # --- ΕΓΓΡΑΦΗ ---
    if not predictions:
        predictions.append("INFO|Δεν βρέθηκαν αγώνες και στα δύο API σήμερα.|-, -, -, -")

    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        now = datetime.now()
        f.write(f"ΗΜΕΡΟΜΗΝΙΑ|{now.strftime('%d/%m/%Y')}|{now.strftime('%H:%M')} (GR)\n")
        for p in predictions:
            f.write(p + "\n")

if __name__ == "__main__":
    fetch_data()
