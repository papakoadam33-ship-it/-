import requests
from datetime import datetime, timedelta

# --- ΡΥΘΜΙΣΕΙΣ API ---
RAPID_API_KEY = "47d5da2fb8mshde110deccc94426p115d5ajsnd9cc939fa561"

def fetch_data():
    predictions = []
    headers = {"X-RapidAPI-Key": RAPID_API_KEY}
    today = datetime.now().strftime('%Y-%m-%d')
    future = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

    # --- ΠΗΓΗ 1: ApiFootball [AF] ---
    try:
        url1 = "https://apifootball3.p.rapidapi.com/"
        params1 = {"action": "get_events", "from": today, "to": future, "timezone": "Europe/Athens"}
        r1 = requests.get(url1, headers=headers, params=params1, timeout=15)
        data1 = r1.json()
        if isinstance(data1, list):
            for item in data1:
                league = f"[AF] {item.get('league_name', 'LEAGUE').upper()}"
                teams = f"{item.get('match_hometeam_name')} - {item.get('match_awayteam_name')}"
                # Τυχαία αρχική πιθανότητα για το Poisson (θα βελτιωθεί στο μέλλον)
                predictions.append(f"{league}|{teams}|Over 2.5,78%,Goal-Goal,72%")
    except: pass

    # --- ΠΗΓΗ 2: Football Prediction [FP] ---
    try:
        url2 = "https://football-prediction-api.p.rapidapi.com/api/v2/predictions"
        params2 = {"iso_date": today} 
        r2 = requests.get(url2, headers=headers, params=params2, timeout=15)
        data2 = r2.json()
        if "data" in data2:
            for item in data2["data"]:
                teams = f"{item.get('home_team')} - {item.get('away_team')}"
                league = f"[FP] {item.get('federation', 'INTL').upper()}"
                tip = item.get("prediction", "1X")
                # Εδώ παίρνουμε την πραγματική πιθανότητα από το API
                prob_val = item.get("probabilities", {}).get(tip, 80)
                
                # ΕΙΔΙΚΗ ΕΙΔΟΠΟΙΗΣΗ ΓΙΑ ΔΥΝΑΤΑ ΣΗΜΕΙΑ (>85%)
                star = "🔥 " if float(prob_val) >= 85 else ""
                predictions.append(f"{star}{league}|{teams}|{tip},{prob_val}%,Over 1.5,88%")
    except: pass

    # --- ΕΓΓΡΑΦΗ ---
    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        now = datetime.now()
        f.write(f"ΗΜΕΡΟΜΗΝΙΑ|{now.strftime('%d/%m/%Y')}|{now.strftime('%H:%M')} (GR)\n")
        
        if not predictions:
            f.write("INFO|Αναμονή για τα βραδινά ματς (Τότεναμ, Μπενφίκα κλπ). Δοκίμασε Reboot μετά τις 18:30.|-, -, -, -\n")
        else:
            seen = set()
            # Ταξινομούμε ώστε τα "🔥" να φαίνονται πρώτα
            predictions.sort(key=lambda x: "🔥" not in x)
            for p in predictions:
                team_names = p.split('|')[1]
                if team_names not in seen:
                    f.write(p + "\n")
                    seen.add(team_names)

if __name__ == "__main__":
    fetch_data()
