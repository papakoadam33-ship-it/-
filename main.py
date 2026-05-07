import requests
import time
from datetime import datetime, timedelta

# Το κλειδί σου από το RapidAPI
API_KEY = "47d5da2fb8mshde110deccc94426p115d5ajsnd9cc939fa561"

# Τα πρωταθλήματα που θέλουμε
LEAGUE_IDS = [39, 140, 135, 71, 128, 94, 197]

def get_smart_tip(home, away):
    # Μια απλή λογική για να βγάζει διαφορετικά σημεία
    score = len(home) + len(away)
    if score % 3 == 0: return "Over 1.5"
    if score % 3 == 1: return "Goal-Goal"
    return "1X & Over 1.5"

def get_predictions():
    # Σωστό URL για RapidAPI
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }
    
    today = datetime.now().strftime('%Y-%m-%d')
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    
    content = f"📅 Marios Pro Tips\nΕνημέρωση: {datetime.now().strftime('%d/%m %H:%M')}\n\n"
    found = False

    for lid in LEAGUE_IDS:
        params = {"league": str(lid), "next": "10"}
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                data = response.json()
                matches = data.get('response', [])
                if matches:
                    content += f"--- {matches[0]['league']['name']} ---\n"
                    for m in matches:
                        m_date = m['fixture']['date'][:10]
                        if m_date == today or m_date == tomorrow:
                            h = m['teams']['home']['name']
                            a = m['teams']['away']['name']
                            day = "Σήμερα" if m_date == today else "Αύριο"
                            content += f"⚽ [{day}] {h} vs {a} -> {get_smart_tip(h, a)}\n"
                            found = True
                    content += "\n"
            
            # ΠΕΡΙΜΕΝΟΥΜΕ 7 ΔΕΥΤΕΡΟΛΕΠΤΑ (Επειδή το πλάνο σου έχει όριο 10/λεπτό)
            time.sleep(7) 
            
        except Exception as e:
            print(f"Σφάλμα: {e}")

    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        f.write(content if found else "Δεν βρέθηκαν αγώνες για σήμερα/αύριο.")

if __name__ == "__main__":
    get_predictions()

