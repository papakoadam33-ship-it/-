import requests
from datetime import datetime, timedelta

# Αντέγραψε το κλειδί από την εικόνα σου και βάλ' το εδώ
API_KEY = "03411e3ab539f7c9723807379af72b61"

# Τα IDs για τα πρωταθλήματα που ζήτησες:
# 39: Premier League, 140: La Liga, 135: Serie A, 71: Βραζιλία, 128: Αργεντινή, 94: Πορτογαλία, 197: Ελλάδα
LEAGUE_IDS = [39, 140, 135, 71, 128, 94, 197]

def get_smart_tip(home_name, away_name):
    """Μια απλή λογική για ποικιλία στα προγνωστικά"""
    combined = len(home_name) + len(away_name)
    if combined % 4 == 0: return "Goal-Goal"
    if combined % 4 == 1: return "1X & Over 1.5"
    if combined % 4 == 2: return "Over 2.5"
    return "2-3 Goals"

def get_predictions():
    # Στο API-Football χρησιμοποιούμε αυτό το URL για επερχόμενα ματς
    url = "https://v3.football.api-sports.io/fixtures"
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': 'v3.football.api-sports.io'
    }
    
    # Ημερομηνίες για σήμερα και αύριο
    today = datetime.now().strftime('%Y-%m-%d')
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    
    all_content = f"📅 Marios Pro Tips\nΕνημέρωση: {datetime.now().strftime('%d/%m %H:%M')}\n\n"
    found_any = False

    for league_id in LEAGUE_IDS:
        # Ζητάμε τα ματς του συγκεκριμένου πρωταθλήματος για σήμερα και αύριο
        params = {'league': league_id, 'next': 10}
        
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                data = response.json()
                matches = data.get('response', [])
                
                if matches:
                    league_name = matches[0]['league']['name']
                    league_content = f"--- {league_name} ---\n"
                    has_league_matches = False
                    
                    for m in matches:
                        match_date = m['fixture']['date'][:10]
                        # Κρατάμε μόνο σήμερα και αύριο
                        if match_date == today or match_date == tomorrow:
                            home = m['teams']['home']['name']
                            away = m['teams']['away']['name']
                            day_label = "Σήμερα" if match_date == today else "Αύριο"
                            
                            tip = get_smart_tip(home, away)
                            league_content += f"⚽ [{day_label}] {home} vs {away} -> {tip}\n"
                            has_league_matches = True
                            found_any = True
                    
                    if has_league_matches:
                        all_content += league_content + "\n"
            
        except Exception as e:
            print(f"Error league {league_id}: {e}")

    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        if found_any:
            f.write(all_content)
        else:
            f.write(f"📅 {today}\nΔεν βρέθηκαν προγραμματισμένοι αγώνες για σήμερα ή αύριο.")

if __name__ == "__main__":
    get_predictions()

