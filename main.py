import requests
from datetime import datetime, timedelta

# --- ΡΥΘΜΙΣΕΙΣ API ---
RAPID_API_KEY = "47d5da2fb8mshde110deccc94426p115d5ajsnd9cc939fa561"

def fetch_data():
    predictions = []
    headers = {"X-RapidAPI-Key": RAPID_API_KEY}
    today = datetime.now().strftime('%Y-%m-%d')
    
    # --- ΠΗΓΗ 1: ApiFootball (Deep Scan) ---
    try:
        # Χρησιμοποιούμε το 'get_predictions' που είναι πιο αναλυτικό για προγνωστικά
        url1 = "https://apifootball3.p.rapidapi.com/"
        params1 = {"action": "get_predictions", "from": today, "to": today}
        r1 = requests.get(url1, headers=headers, params=params1, timeout=15)
        data1 = r1.json()
        
        if isinstance(data1, list):
            for item in data1:
                home = item.get('match_hometeam_name')
                away = item.get('match_awayteam_name')
                league = f"[AF] {item.get('league_name', 'FOOTBALL')}"
                prob_o = item.get('prob_O', '75')
                prob_bts = item.get('prob_bts', '65')
                predictions.append(f"{league}|{home} - {away}|Over 2.5,{prob_o}%,GG,{prob_bts}%")
    except Exception as e:
        print(f"Error Source 1: {e}")

    # --- ΠΗΓΗ 2: Football Prediction (All Markets) ---
    try:
        url2 = "https://football-prediction-api.p.rapidapi.com/api/v2/predictions"
        # Αφαιρούμε το market=classic για να φέρει ό,τι έχει διαθέσιμο
        params2 = {"iso_date": today}
        r2 = requests.get(url2, headers=headers, params=params2, timeout=15)
        data2 = r2.json()
        
        if "data" in data2:
            for item in data2["data"]:
                home = item.get('home_team')
                away = item.get('away_team')
                fed = f"[FP] {item.get('federation', 'INTL')}"
                pred = item.get('prediction', '1X')
                # Προσπαθούμε να βρούμε την πιθανότητα αν υπάρχει
                prob_val = "80"
                if "probabilities" in item and pred in item["probabilities"]:
                    prob_val = item["probabilities"][pred]
                
                predictions.append(f"{fed}|{home} - {away}|{pred},{prob_val}%,Over 1.5,85%")
    except Exception as e:
        print(f"Error Source 2: {e}")

    # --- ΕΓΓΡΑΦΗ ΣΤΟ ΑΡΧΕΙΟ ---
    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        now = datetime.now()
        # Η πρώτη γραμμή είναι πάντα η ημερομηνία/ώρα για το app.py
        f.write(f"ΗΜΕΡΟΜΗΝΙΑ|{now.strftime('%d/%m/%Y')}|{now.strftime('%H:%M')} (GR)\n")
        
        if not predictions:
            # Αν δεν βρέθηκε τίποτα, γράφουμε το μήνυμα αναμονής
            f.write("INFO|Αναμονή για ενημέρωση των δωρεάν API. (Τα ματς Τότεναμ/Μπενφίκα μπορεί να μην υποστηρίζονται στο Free πλάνο).|-, -, -, -\n")
        else:
            # Αφαίρεση διπλότυπων βάσει ονομάτων ομάδων
            seen = set()
            for p in predictions:
                match_id = p.split('|')[1]
                if match_id not in seen:
                    f.write(p + "\n")
                    seen.add(match_id)

if __name__ == "__main__":
    fetch_data()
