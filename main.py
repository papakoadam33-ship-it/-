import requests
import time
from datetime import datetime, timedelta

API_KEY = "47d5da2fb8mshde110deccc94426p115d5ajsnd9cc939fa561"
# Πρωταθλήματα: Αγγλία, Ισπανία, Ιταλία, Βραζιλία, Αργεντινή, Πορτογαλία, Ελλάδα
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
    
    # Ζητάμε αγώνες από σήμερα μέχρι και μετά από 10 ημέρες
    from_date = datetime.now().strftime('%Y-%m-%d')
    to_date = (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d')
    
    content = f"📅 Marios Pro Tips\nΕνημέρωση: {datetime.now().strftime('%H:%M')}\n\n"
    found = False

    for lid in LEAGUE_IDS:
        # Χρησιμοποιούμε ημερομηνίες αντί για 'next' για να είμαστε σίγουροι
        params = {"league": str(lid), "from": from_date, "to": to_date}
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                data = response.json()
                matches = data.get('response', [])
                if matches:
                    # Παίρνουμε μόνο τους πρώτους 5 αγώνες από κάθε λίγκα για να μην γεμίσει πολύ
                    content += f"--- {matches[0]['league']['name']} ---\n"
                    for m in matches[:5]:
                        h = m['teams']['home']['name']
                        a = m['teams']['away']['name']
                        m_date = m['fixture']['date'][8:10] + "/" + m['fixture']['date'][5:7]
                        
                        content += f"⚽ [{m_date}] {h} vs {a} -> {get_smart_tip(h, a)}\n"
                        found = True
                    content += "\n"
            
            time.sleep(7) # Πολύ σημαντικό για το δωρεάν πλάνο σου
            
        except Exception as e:
            print(f"Σφάλμα: {e}")

    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        f.write(content if found else "Δεν βρέθηκαν αγώνες για τις επόμενες 10 ημέρες.")

if __name__ == "__main__":
    get_predictions()

