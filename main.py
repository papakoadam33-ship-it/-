import requests
import time
from datetime import datetime

# Ρυθμίσεις API - RapidAPI Football
API_KEY = "47d5da2fb8mshde110deccc94426p115d5ajsnd9cc939fa561"
HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

# Επιλογή πρωταθλημάτων που έχουν σχεδόν πάντα αγώνες (π.χ. Βραζιλία, ΗΠΑ, Μεξικό)
LEAGUE_IDS = [71, 253, 262, 39, 140, 197]

def get_advice(fid):
    url = "https://api-football-v1.p.rapidapi.com/v3/predictions"
    try:
        time.sleep(1.2) # Καθυστέρηση για το Free Tier
        res = requests.get(url, headers=HEADERS, params={"fixture": fid})
        data = res.json()
        if data.get('response'):
            return data['response'][0]['predictions']['advice']
    except:
        pass
    return "Goal-Goal or Over 1.5"

def run():
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    all_content = f"⚽ MARIOS PRO TIPS\nΕνημέρωση: {datetime.now().strftime('%d/%m %H:%M')}\n"
    all_content += "="*30 + "\n\n"
    
    found = False
    for lid in LEAGUE_IDS:
        # Ζητάμε τους επόμενους 10 αγώνες (next=10) για να μην είναι ποτέ άδειο
        params = {"league": str(lid), "next": "10"}
        try:
            response = requests.get(url, headers=HEADERS, params=params)
            matches = response.json().get('response', [])
            if matches:
                all_content += f"🏆 {matches[0]['league']['name']}\n"
                for m in matches[:3]:
                    h, a = m['teams']['home']['name'], m['teams']['away']['name']
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
            f.write("Δεν βρέθηκαν επερχόμενοι αγώνες. Δοκιμάστε αργότερα.")

if __name__ == "__main__":
    run()

