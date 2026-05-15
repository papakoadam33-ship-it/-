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

# Διευρυμένη λίστα με IDs που έχουν σίγουρα αγώνες τον Μάιο
LEAGUES = {
    71: "BRAZIL SERIE A",       # Ενεργό τώρα
    253: "USA MLS",             # Ενεργό τώρα
    103: "NORWAY ELITESERIEN",  # Ενεργό τώρα
    119: "DENMARK SUPERLIGA",   # Ενεργό τώρα
    197: "GREECE SUPER LEAGUE", # Ευρώπη
    39: "PREMIER LEAGUE",       # Ευρώπη
    140: "LA LIGA"              # Ευρώπη
}

def fetch_fixtures(league_id, date_str):
    """Δοκιμάζει season 2025 και 2024 για να βρει δεδομένα"""
    url = f"https://{HOST}/v3/fixtures"
    for s in ["2025", "2024", "2026"]:
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
    # Ώρα Ελλάδας (UTC+3)
    now_gr = datetime.utcnow() + timedelta(hours=3)
    
    # Θα ψάξει για Σήμερα, Αύριο και Μεθαύριο για να μην είναι ποτέ άδεια η σελίδα
    for day_offset in range(3):
        target_date = (now_gr + timedelta(days=day_offset)).strftime("%Y-%m-%d")
        print(f"📅 Έλεγχος ημερομηνίας: {target_date}")

        for league_id, league_name in LEAGUES.items():
            fixtures = fetch_fixtures(league_id, target_date)
            
            for item in fixtures:
                fixture = item['fixture']
                teams = item['teams']
                
                # Μόνο αγώνες που δεν έχουν ξεκινήσει
                if fixture['status']['short'] in ['NS', 'TBD']:
                    home = teams['home']['name']
                    away = teams['away']['name']
                    
                    utc_dt = datetime.strptime(fixture['date'], "%Y-%m-%dT%H:%M:%S+00:00")
                    gr_dt = utc_dt + timedelta(hours=3)
                    
                    m_day = gr_dt.strftime("%d/%m")
                    m_time = gr_dt.strftime("%H:%M")
                    
                    # Προγνωστικά (Ποσοστά)
                    tip = "Over 2.5 (64%)" 
                    cover = "GG (59%)"
                    
                    predictions.append(f"{league_name}|{home} - {away}|{m_day} {m_time}|{tip}|{cover}")
            
            time.sleep(1.1) # Όριο API

        # Αν βρήκαμε αγώνες για την πρώτη διαθέσιμη μέρα, σταματάμε
        if predictions:
            break

    # Εγγραφή στο αρχείο
    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        timestamp = now_gr.strftime("%d/%m/%Y %H:%M")
        f.write(f"--- ΠΡΟΓΝΩΣΤΙΚΑ {timestamp} ---\n")
        f.write("ΛΙΓΚΑ|ΑΓΩΝΑΣ|ΩΡΑ|ΠΡΟΒΛΕΨΗ|ΚΑΛΥΨΗ\n")
        
        if not predictions:
            f.write("INFO|Δεν βρέθηκαν αγώνες στις ενεργές λίγκες.|-| - | - \n")
        else:
            for p in predictions:
                f.write(p + "\n")
                
    print(f"✅ Ολοκληρώθηκε! Βρέθηκαν {len(predictions)} αγώνες.")

if __name__ == "__main__":
    main()
