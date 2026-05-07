import requests
import time
from datetime import datetime

API_KEY = "47d5da2fb8mshde110deccc94426p115d5ajsnd9cc939fa561"
LEAGUE_IDS = [39, 140, 135, 71, 128, 94, 197]

def get_smart_tip(home, away):
    score = len(home) + len(away)
    if score % 3 == 0: return "Over 1.5"
    if score % 3 == 1: return "Goal-Goal"
    return "1X & Over 1.5"

def get_predictions():
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }
    
    content = f"📅 Marios Pro Tips\nΕνημέρωση: {datetime.now().strftime('%H:%M')}\n\n"
    found = False

    for lid in LEAGUE_IDS:
        params = {"league": str(lid), "next": "10"} # Ζητάμε τους 10 επόμενους
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                data = response.json()
                matches = data.get('response', [])
                if matches:
                    content += f"--- {matches[0]['league']['name']} ---\n"
                    for m in matches:
                        h = m['teams']['home']['name']
                        a = m['teams']['away']['name']
                        # Παίρνουμε την ημερομηνία για να την βλέπουμε
                        raw_date = m['fixture']['date'][5:10] # π.χ. 05-08
                        formatted_date = raw_date.replace("-", "/")
                        
                        content += f"⚽ [{formatted_date}] {h} vs {a} -> {get_smart_tip(h, a)}\n"
                        found = True
                    content += "\n"
            
            time.sleep(7) # Αναμονή για το όριο του RapidAPI
            
        except Exception as e:
            print(f"Σφάλμα: {e}")

    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        f.write(content if found else "Το API είναι άδειο. Δοκίμασε σε λίγο.")

if __name__ == "__main__":
    get_predictions()


