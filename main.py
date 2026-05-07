import requests
import time
from datetime import datetime, timedelta

# Το κλειδί σου από το RapidAPI
API_KEY = "47d5da2fb8mshde110deccc94426p115d5ajsnd9cc939fa561"

# Πρωταθλήματα που παρακολουθούμε
LEAGUE_IDS = [39, 140, 135, 71, 128, 94, 197]

def get_smart_tip(home, away):
    combined = len(home) + len(away)
    if combined % 3 == 0: return "Over 1.5"
    if combined % 3 == 1: return "Goal-Goal"
    return "1X & Over 1.5"

def get_predictions():
    # Σωστό URL για RapidAPI σύμφωνα με τη συνδρομή σου
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }
    
    # Εύρος 7 ημερών για να βρούμε σίγουρα αγώνες
    from_date = datetime.now().strftime('%Y-%m-%d')
    to_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
    
    all_content = f"📅 Marios Pro Tips\nΕνημέρωση: {datetime.now().strftime('%H:%M')}\n\n"
    found_any = False

    for lid in LEAGUE_IDS:
        params = {"league": str(lid), "from": from_date, "to": to_date}
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                data = response.json()
                matches = data.get('response', [])
                if matches:
                    all_content += f"--- {matches[0]['league']['name']} ---\n"
                    for m in matches[:5]:
                        h, a = m['teams']['home']['name'], m['teams']['away']['name']
                        m_date = m['fixture']['date'][8:10] + "/" + m['fixture']['date'][5:7]
                        tip = get_smart_tip(h, a)
                        all_content += f"⚽ [{m_date}] {h} vs {a} -> {tip}\n"
                        found_any = True
                    all_content += "\n"
            
            # Αναμονή 7 δευτερολέπτων για να μην ξεπεράσουμε το όριο των 10 αιτημάτων/λεπτό
            time.sleep(7) 
            
        except Exception as e:
            print(f"Error: {e}")

    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        f.write(all_content if found_any else "Δεν βρέθηκαν επερχόμενοι αγώνες.")

if __name__ == "__main__":
    get_predictions()

