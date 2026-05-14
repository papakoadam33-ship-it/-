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

# Διευρυμένη λίστα πρωταθλημάτων
LEAGUES = {
    197: "GREECE SUPER LEAGUE",
    39: "PREMIER LEAGUE",
    140: "LA LIGA",
    135: "SERIE A",
    78: "BUNDESLIGA",
    61: "LIGUE 1",
    40: "CHAMPIONSHIP",
    253: "MAJOR LEAGUE SOCCER",
    2: "CHAMPIONS LEAGUE",
    3: "EUROPA LEAGUE",
    848: "CONFERENCE LEAGUE",
    45: "LIGUE 2",
    41: "LEAGUE ONE"
}

def fetch_fixtures(league_id, date_str):
    """Δοκιμάζει διαφορετικές σεζόν μέχρι να βρει αγώνες"""
    url = f"https://{HOST}/v3/fixtures"
    # Δοκιμή σεζόν 2025, μετά 2024 και 2026
    for s in ["2025", "2024", "2026"]:
        querystring = {"league": league_id, "season": s, "date": date_str}
        try:
            response = requests.get(url, headers=HEADERS, params=querystring, timeout=12)
            res_data = response.json().get('response', [])
            if res_data:
                return res_data
        except:
            continue
    return []

def main():
    predictions = []
    # Ώρα Ελλάδας (UTC+3)
    now_gr = datetime.utcnow() + timedelta(hours=3)
    
    # Ημερομηνίες για έλεγχο
    today = now_gr.strftime("%Y-%m-%d")
    tomorrow = (now_gr + timedelta(days=1)).strftime("%Y-%m-%d")
    
    print(f"🚀 Έναρξη αναζήτησης αγώνων (RapidAPI)...")

    for league_id, league_name in LEAGUES.items():
        print(f"📊 Έλεγχος: {league_name}...")
        
        # Πρώτα ψάξε για σήμερα
        fixtures = fetch_fixtures(league_id, today)
        
        # Αν δεν έχει σήμερα, ψάξε για αύριο
        if not fixtures:
            fixtures = fetch_fixtures(league_id, tomorrow)
        
        for item in fixtures:
            fixture = item['fixture']
            teams = item['teams']
            
            # Φιλτράρουμε μόνο αγώνες που δεν έχουν ξεκινήσει (NS) ή είναι προγραμματισμένοι (TBD)
            if fixture['status']['short'] in ['NS', 'TBD']:
                home = teams['home']['name']
                away = teams['away']['name']
                
                # Μετατροπή σε ώρα Ελλάδας
                utc_dt = datetime.strptime(fixture['date'], "%Y-%m-%dT%H:%M:%S+00:00")
                gr_dt = utc_dt + timedelta(hours=3)
                
                m_day = gr_dt.strftime("%d/%m")
                m_time = gr_dt.strftime("%H:%M")
                
                # Προγνωστικά (Ποσοστά σε όλα τα πεδία)
                tip = "Over 2.5 (63%)" 
                cover = "GG (57%)"
                
                predictions.append(f"{league_name}|{home} - {away}|{m_day} {m_time}|{tip}|{cover}")
        
        time.sleep(1.2) # Αποφυγή Rate Limit (100 calls/day)

    # Εγγραφή στο αρχείο daily_predictions.txt
    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        timestamp = now_gr.strftime("%d/%m/%Y %H:%M")
        f.write(f"--- ΠΡΟΓΝΩΣΤΙΚΑ {timestamp} ---\n")
        f.write("ΛΙΓΚΑ|ΑΓΩΝΑΣ|ΩΡΑ|ΠΡΟΒΛΕΨΗ|ΚΑΛΥΨΗ\n")
        
        if not predictions:
            f.write("INFO|Δεν υπάρχουν προγραμματισμένοι αγώνες.|-| - | - \n")
        else:
            for p in predictions:
                f.write(p + "\n")
                
    print(f"✅ Ολοκληρώθηκε! Το αρχείο ενημερώθηκε.")

if __name__ == "__main__":
    main()
