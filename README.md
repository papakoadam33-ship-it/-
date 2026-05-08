import requests
import time
from datetime import datetime

# Ρυθμίσεις API - Χρησιμοποιούμε το δικό σου κλειδί RapidAPI
API_KEY = "47d5da2fb8mshde110deccc94426p115d5ajsnd9cc939fa561"
HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

# Λίστα με σίγουρα πρωταθλήματα (Αγγλία, Ισπανία, Ιταλία, Γερμανία, Γαλλία, Βραζιλία)
LEAGUE_IDS = [39, 140, 135, 78, 61, 71]

def get_advice(fixture_id):
    url = "https://api-football-v1.p.rapidapi.com/v3/predictions"
    try:
        time.sleep(1.1) # Για να μην φάμε block
        res = requests.get(url, headers=HEADERS, params={"fixture": fixture_id})
        data = res.json()
        if data['response']:
            return data['response'][0]['predictions']['advice']
    except:
        pass
    return "Over 1.5 Goals"

def run():
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    all_content = f"⚽ MARIOS PRO TIPS\nΕνημέρωση: {datetime.now().strftime('%d/%m %H:%M')}\n"
    all_content += "="*30 + "\n\n"
    
    found = False
    for lid in LEAGUE_IDS:
        # Παίρνουμε τους επόμενους 5 αγώνες για κάθε λίγκα
        params = {"league": str(lid), "next": "5"}
        try:
            response = requests.get(url, headers=HEADERS, params=params)
            matches = response.json().get('response', [])
            if matches:
                all_content += f"🏆 {matches[0]['league']['name']}\n"
                for m in matches[:3]:
                    h = m['teams']['home']['name']
                    a = m['teams']['away']['name']
                    fid = m['fixture']['id']
                    advice = get_advice(fid)
                    all_content += f"🔹 {h} - {a} ➔ {advice}\n"
                    found = True
                all_content += "\n"
            time.sleep(1)
        except:
            continue

    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        if found:
            f.write(all_content)
        else:
            f.write("Δεν βρέθηκαν αγώνες. Ελέγξτε το API Key.")

if __name__ == "__main__":
    run()
