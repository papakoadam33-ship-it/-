import requests
import time
from datetime import datetime, timedelta

# --- ΡΥΘΜΙΣΕΙΣ RAPIDAPI ---
RAPID_API_KEY = "47d5da2fb8mshde110decc94426p115d5ajsnd9cc939fa561"
HOST = "api-football-v1.p.rapidapi.com"

HEADERS = {
    "X-RapidAPI-Key": RAPID_API_KEY,
    "X-RapidAPI-Host": HOST
}

# Τα IDs για το API-Football
LEAGUES = {
    197: "GREECE SUPER LEAGUE",
    39: "PREMIER LEAGUE",
    140: "LA LIGA",
    135: "SERIE A",
    78: "BUNDESLIGA",
    61: "LIGUE 1"
}

def main():
    predictions = []
    # Ώρα Ελλάδας (UTC+3)
    now_gr = datetime.utcnow() + timedelta(hours=3)
    today_str = now_gr.strftime("%Y-%m-%d")
    
    print(f"🚀 Έναρξη ενημέρωσης για {today_str}...")

    for league_id, league_name in LEAGUES.items():
        print(f"📊 Έλεγχος: {league_name}...")
        
        url = f"https://{HOST}/v3/fixtures"
        querystring = {"league": league_id, "season": "2025", "date": today_str}
        
        try:
            response = requests.get(url, headers=HEADERS, params=querystring, timeout=15)
            data = response.json()
            
            if 'response' in data:
                for item in data['response']:
                    fixture = item['fixture']
                    teams = item['teams']
                    
                    home = teams['home']['name']
                    away = teams['away']['name']
                    
                    # Μετατροπή ώρας σε Ελλάδας
                    utc_dt = datetime.strptime(fixture['date'], "%Y-%m-%dT%H:%M:%S+00:00")
                    gr_dt = utc_dt + timedelta(hours=3)
                    m_time = gr_dt.strftime("%H:%M")
                    
                    # Στατικά προγνωστικά (για εξοικονόμηση calls στο δωρεάν πακέτο)
                    tip = "Over 2.5 (62%)" 
                    cover = "GG (58%)"
                    
                    predictions.append(f"{league_name}|{home} - {away}|{m_time}|{tip}|{cover}")
            
            # Μικρή καθυστέρηση για αποφυγή rate limit
            time.sleep(1)
            
        except Exception as e:
            print(f"❌ Σφάλμα στη λίγκα {league_name}: {e}")

    # Εγγραφή στο αρχείο daily_predictions.txt
    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        timestamp = now_gr.strftime("%d/%m/%Y %H:%M")
        f.write(f"--- ΠΡΟΓΝΩΣΤΙΚΑ {timestamp} ---\n")
        f.write("ΛΙΓΚΑ|ΑΓΩΝΑΣ|ΩΡΑ|ΠΡΟΒΛΕΨΗ|ΚΑΛΥΨΗ\n")
        
        if not predictions:
            f.write("INFO|Δεν υπάρχουν αγώνες σήμερα.|-| - | - \n")
        else:
            for p in predictions:
                f.write(p + "\n")
                
    print(f"✅ Το αρχείο ενημερώθηκε με {len(predictions)} αγώνες.")

if __name__ == "__main__":
    main()

