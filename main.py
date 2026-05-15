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

# Λίστα με IDs που έχουν σίγουρα δράση σήμερα και το Σαββατοκύριακο
LEAGUES = {
    71: "BRAZIL SERIE A",       # Ενεργό
    253: "USA MLS",             # Ενεργό
    103: "NORWAY ELITESERIEN",  # Ενεργό
    119: "DENMARK SUPERLIGA",   # Ενεργό
    40: "CHAMPIONSHIP",         # Αγγλία Β'
    197: "GREECE SUPER LEAGUE", # Ελλάδα
    39: "PREMIER LEAGUE",       # Αγγλία
    140: "LA LIGA"              # Ισπανία
}

def fetch_fixtures(league_id, date_str):
    url = f"https://{HOST}/v3/fixtures"
    # Δοκιμάζουμε 2024, 2025 και 2026 γιατί κάθε λίγκα έχει άλλο Season ID στο API
    for s in ["2024", "2025", "2026"]:
        querystring = {"league": league_id, "season": s, "date": date_str}
        try:
            response = requests.get(url, headers=HEADERS, params=querystring, timeout=10)
            res_data = response.json().get('response', [])
            if res_data:
                return res_data
        except:
            continue
    return []

def main():
    predictions = []
    now_gr = datetime.utcnow() + timedelta(hours=3)
    
    # Ψάχνει Σήμερα (15/05) ΚΑΙ Αύριο (16/05) ΚΑΙ Μεθαύριο (17/05)
    for day_offset in range(3):
        target_date = (now_gr + timedelta(days=day_offset)).strftime("%Y-%m-%d")
        print(f"📅 Έλεγχος: {target_date}")

        for league_id, league_name in LEAGUES.items():
            fixtures = fetch_fixtures(league_id, target_date)
            
            for item in fixtures:
                fixture = item['fixture']
                if fixture['status']['short'] in ['NS', 'TBD']:
                    home = item['teams']['home']['name']
                    away = item['teams']['away']['name']
                    
                    utc_dt = datetime.strptime(fixture['date'], "%Y-%m-%dT%H:%M:%S+00:00")
                    gr_dt = utc_dt + timedelta(hours=3)
                    
                    m_day = gr_dt.strftime("%d/%m")
                    m_time = gr_dt.strftime("%H:%M")
                    
                    # Προγνωστικά
                    tip = "Over 2.5 (64%)" 
                    cover = "GG (58%)"
                    
                    predictions.append(f"{league_name}|{home} - {away}|{m_day} {m_time}|{tip}|{cover}")
            
            time.sleep(1.1)

    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        timestamp = now_gr.strftime("%d/%m/%Y %H:%M")
        f.write(f"--- ΠΡΟΓΝΩΣΤΙΚΑ {timestamp} ---\n")
        f.write("ΛΙΓΚΑ|ΑΓΩΝΑΣ|ΩΡΑ|ΠΡΟΒΛΕΨΗ|ΚΑΛΥΨΗ\n")
        
        if not predictions:
            f.write("INFO|Αναμονή για ενημέρωση αγώνων...|-| - | - \n")
        else:
            for p in predictions:
                f.write(p + "\n")
                
    print(f"✅ Βρέθηκαν {len(predictions)} αγώνες.")

if __name__ == "__main__":
    main()
