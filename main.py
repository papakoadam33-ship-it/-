
import requests
from datetime import datetime, timedelta

# Το κλειδί σου από το RapidAPI
API_KEY = "47d5da2fb8mshde110deccc94426p115d5ajsnd9cc939fa561"

# IDs Πρωταθλημάτων: Αγγλία, Ισπανία, Ιταλία, Βραζιλία, Αργεντινή, Πορτογαλία, Ελλάδα
LEAGUE_IDS = [39, 140, 135, 71, 128, 94, 197]

def get_smart_tip(home_name, away_name):
    """Απλή λογική για προγνωστικά"""
    combined = len(home_name) + len(away_name)
    if combined % 4 == 0: return "Goal-Goal"
    if combined % 4 == 1: return "1X & Over 1.5"
    if combined % 4 == 2: return "Over 2.5"
    return "2-3 Goals"

def get_predictions():
    # Προσοχή: Για RapidAPI το host αλλάζει ελαφρώς
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }
    
    today = datetime.now().strftime('%Y-%m-%d')
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    
    all_content = f"📅 Marios Pro Tips (RapidAPI)\nΕνημέρωση: {datetime.now().strftime('%d/%m %H:%M')}\n\n"
    found_any = False

    for league_id in LEAGUE_IDS:
        # Παίρνουμε τους επόμενους 10 αγώνες για κάθε πρωτάθλημα
        params = {"league": str(league_id), "next": "10"}
        
        try:
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                matches = data.get('response', [])
                
                if matches:
                    league_name = matches[0]['league']['name']
                    league_content = f"--- {league_name} ---\n"
                    has_matches = False
                    
                    for m in matches:
                        match_date = m['fixture']['date'][:10]
                        # Φιλτράρουμε μόνο για σήμερα και αύριο
                        if match_date == today or match_date == tomorrow:
                            home = m['teams']['home']['name']
                            away = m['teams']['away']['name']
                            day_label = "Σήμερα" if match_date == today else "Αύριο"
                            
                            tip = get_smart_tip(home, away)
                            league_content += f"⚽ [{day_label}] {home} vs {away} -> {tip}\n"
                            has_matches = True
                            found_any = True
                    
                    if has_matches:
                        all_content += league_content + "\n"
            else:
                print(f"Σφάλμα στο πρωτάθλημα {league_id}: {response.status_code}")

        except Exception as e:
            print(f"Error: {e}")

    # Αποθήκευση στο αρχείο
    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        if found_any:
            f.write(all_content)
        else:
            f.write(f"📅 {today}\nΔεν βρέθηκαν αγώνες για σήμερα/αύριο. Βεβαιώσου ότι έχεις πατήσει 'Subscribe to Free Plan' στο RapidAPI.")

if __name__ == "__main__":
    get_predictions()
