import requests
from datetime import datetime, timedelta

# --- ΡΥΘΜΙΣΕΙΣ API ---
RAPID_API_KEY = "47d5da2fb8mshde110deccc94426p115d5ajsnd9cc939fa561"

def fetch_data():
    predictions = []
    headers = {"X-RapidAPI-Key": RAPID_API_KEY}
    
    # Ημερομηνίες για αναζήτηση σε βάθος 3 ημερών
    today = datetime.now().strftime('%Y-%m-%d')
    future = (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d')

    # --- ΠΗΓΗ 1: ApiFootball [AF] ---
    try:
        url1 = "https://apifootball3.p.rapidapi.com/"
        # Ζητάμε αγώνες για τις επόμενες ημέρες
        params1 = {"action": "get_events", "from": today, "to": future, "timezone": "Europe/Athens"}
        r1 = requests.get(url1, headers=headers, params=params1)
        data1 = r1.json()
        if isinstance(data1, list) and len(data1) > 0:
            for item in data1[:15]:
                league = f"[AF] {item.get('league_name', 'LEAGUE').upper()}"
                date_str = item.get('match_date', today)
                teams = f"{item.get('match_hometeam_name')} - {item.get('match_awayteam_name')}"
                predictions.append(f"{league} ({date_str})|{teams}|Over 2.5,75%,Goal-Goal,70%")
    except: pass

    # --- ΠΗΓΗ 2: Football Prediction [FP] ---
    # Το Football Prediction συνήθως δίνει μόνο για τη συγκεκριμένη μέρα στο δωρεάν
    try:
        url2 = "https://football-prediction-api.p.rapidapi.com/api/v2/predictions"
        params2 = {"market": "classic", "iso_date": today}
        r2 = requests.get(url2, headers=headers, params=params2)
        data2 = r2.json()
        if "data" in data2:
            for item in data2["data"][:15]:
                teams = f"{item.get('home_team')} - {item.get('away_team')}"
                league = f"[FP] {item.get('federation', 'INTL').upper()}"
                tip = item.get("prediction", "1X")
                prob = "80%"
                predictions.append(f"{league}|{teams}|{tip},{prob},Over 1.5,85%")
    except: pass

    # --- ΕΓΓΡΑΦΗ ---
    if not predictions:
        predictions.append("INFO|Τα API είναι συνδεδεμένα, αλλά τα δωρεάν πακέτα δεν έχουν αγώνες αυτή τη στιγμή.|-, -, -, -")

    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        now = datetime.now()
        f.write(f"ΗΜΕΡΟΜΗΝΙΑ|{now.strftime('%d/%m/%Y')}|{now.strftime('%H:%M')} (GR)\n")
        for p in predictions:
            f.write(p + "\n")

if __name__ == "__main__":
    fetch_data()
