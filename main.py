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

# Λίστα με IDs που έχουν σίγουρα δράση την Παρασκευή
LEAGUES = {
    197: "GREECE SUPER LEAGUE",
    39: "PREMIER LEAGUE",
    140: "LA LIGA",
    135: "SERIE A",
    78: "BUNDESLIGA",
    61: "LIGUE 1",
    62: "LIGUE 2",        # Β' Γαλλίας (Παρασκευή)
    88: "EREDIVISIE",     # Ολλανδία
    94: "PRIMEIRA LIGA",  # Πορτογαλία
    40: "CHAMPIONSHIP"
}

def fetch_fixtures(league_id, date_str):
    """Δοκιμάζει 2025 ΚΑΙ 2024 γιατί μερικές λίγκες δεν έχουν αλλάξει σεζόν στο API"""
    url = f"https://{HOST}/v3/fixtures"
    # Δοκιμάζουμε πρώτα τη σεζόν 2025 και μετά τη 2024
    for season in ["2025", "2024"]:
        querystring = {"league": league_id, "season": season, "date": date_str}
        try:
            response = requests.get(url, headers=HEADERS, params=querystring, timeout=10)
            data = response.json().get('response', [])
            if data:
                return data
        except:
            continue
    return []

def main():
    predictions = []
    now_gr = datetime.utcnow() + timedelta(hours=3)
    today = now_gr.strftime("%Y-%m-%d")
    
    print(f"🚀 Έναρξη: {today}")

    for league_id, league_name in LEAGUES.items():
        print(f"🔎 Έλεγχος: {league_name}...")
        fixtures = fetch_fixtures(league_id, today)
        
        for item in fixtures:
            fixture = item['fixture']
            # NS = Not Started, TBD = To Be Defined
            if fixture['status']['short'] in ['NS', 'TBD']:
                home = item['teams']['home']['name']
                away = item['teams']['away']['name']
                
                utc_dt = datetime.strptime(fixture['date'], "%Y-%m-%dT%H:%M:%S+00:00")
                gr_dt = utc_dt + timedelta(hours=3)
                m_time = gr_dt.strftime("%H:%M")
                
                # Προγνωστικά
                tip = "Over 2.5 (65%)"
                cover = "GG (58%)"
                
                predictions.append(f"{league_name}|{home} - {away}|{m_time}|{tip}|{cover}")
        
        time.sleep(1.2) # Για να μην ξεπεράσουμε το limit

    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        timestamp = now_gr.strftime("%d/%m/%Y %H:%M")
        f.write(f"--- ΠΡΟΓΝΩΣΤΙΚΑ {timestamp} ---\n")
        f.write("ΛΙΓΚΑ|ΑΓΩΝΑΣ|ΩΡΑ|ΠΡΟΒΛΕΨΗ|ΚΑΛΥΨΗ\n")
        if not predictions:
            f.write("INFO|Δεν βρέθηκαν αγώνες. Δοκίμασε αργότερα.|-| - | - \n")
        else:
            for p in predictions:
                f.write(p + "\n")
    
    print(f"✅ Τέλος. Βρέθηκαν {len(predictions)} αγώνες.")

if __name__ == "__main__":
    main()
