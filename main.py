import requests
from datetime import datetime, timedelta
import time

API_KEY = "47d5da2fb8mshde110deccc94426p115d5ajsnd9cc939fa561"
HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

LEAGUE_IDS = [39, 140, 135, 71, 128, 94, 197]

def get_real_prediction(fixture_id):
    """Παίρνει το πραγματικό προγνωστικό για έναν συγκεκριμένο αγώνα"""
    url = "https://api-football-v1.p.rapidapi.com/v3/predictions"
    params = {"fixture": fixture_id}
    
    try:
        response = requests.get(url, headers=HEADERS, params=params)
        if response.status_code == 200:
            data = response.json()
            if data['response']:
                prediction_data = data['response'][0]['predictions']
                advice = prediction_data['advice']
                # Παίρνουμε την πιθανότητα για το αποτέλεσμα που προτείνει
                return f"💡 Tip: {advice}"
        return "💡 Tip: No data available"
    except:
        return "💡 Tip: Analysis error"

def run_pro_tips():
    fixtures_url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    today = datetime.now().strftime('%Y-%m-%d')
    
    output = f"🚀 MARIOS PRO AI TIPS\nΗμερομηνία: {today}\n" + "="*30 + "\n\n"
    
    for league_id in LEAGUE_IDS:
        params = {"league": str(league_id), "date": today} # Παίρνουμε μόνο τα σημερινά
        
        print(f"Αναζήτηση αγώνων για το League ID: {league_id}...")
        response = requests.get(fixtures_url, headers=HEADERS, params=params)
        
        if response.status_code == 200:
            matches = response.json().get('response', [])
            
            for m in matches:
                home = m['teams']['home']['name']
                away = m['teams']['away']['name']
                f_id = m['fixture']['id']
                
                # Καλούμε το API για το προγνωστικό
                tip = get_real_prediction(f_id)
                
                match_info = f"⚽ {home} vs {away}\n{tip}\n"
                output += match_info + "-"*20 + "\n"
                
                print(f"✅ Βρέθηκε: {home} vs {away}")
                time.sleep(1.2) # Καθυστέρηση για το Rate Limit
        
    with open("marios_pro_tips.txt", "w", encoding="utf-8") as f:
        f.write(output)
    
    print("\n✨ Η ανάλυση ολοκληρώθηκε! Δες το αρχείο marios_pro_tips.txt")

if __name__ == "__main__":
    run_pro_tips()

