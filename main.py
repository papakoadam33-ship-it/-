import requests
import time
from datetime import datetime, timedelta

# Το κλειδί σου - Βεβαιώσου ότι είναι το σωστό
API_KEY = "a1a4edf072dc4b2c8153fced44c88de9"

# Προσθέσαμε Βραζιλία (BSA), Πορτογαλία (PPL) και Αργεντινή (CLI - Copa Libertadores/Sudamericana)
# Σημείωση: Το Free Tier του football-data.org έχει περιορισμένα πρωταθλήματα Λατινικής Αμερικής.
LEAGUES = {
    'Premier League': 'PL',
    'La Liga': 'PD',
    'Serie A': 'SA',
    'Bundesliga': 'BL1',
    'Ligue 1': 'FL1',
    'Champions League': 'CL',
    'Brazil Serie A': 'BSA',
    'Portugal Primeira Liga': 'PPL',
    'Copa Libertadores': 'CLI'
}

def get_prediction_logic(home_team, away_team):
    """Λογική για ποικιλία στα προγνωστικά"""
    combined_len = len(home_team) + len(away_team)
    if combined_len % 4 == 0:
        return "Over 2.5"
    elif combined_len % 4 == 1:
        return "Goal-Goal"
    elif combined_len % 4 == 2:
        return "1X & Over 1.5"
    else:
        return "2-3 Goals"

def get_predictions():
    clean_key = str(API_KEY).strip()
    headers = { 'X-Auth-Token': clean_key }
    
    # Ημερομηνίες: Σήμερα και Αύριο
    today = datetime.utcnow().date()
    tomorrow = today + timedelta(days=1)
    
    all_content = f"📅 Προγνωστικά: {today.strftime('%d/%m')} & {tomorrow.strftime('%d/%m')}\n\n"
    
    found_any_match = False

    for league_name, league_code in LEAGUES.items():
        # status=SCHEDULED για να βλέπουμε τα επόμενα ματς
        url = f"https://api.football-data.org/v4/competitions/{league_code}/matches?status=SCHEDULED"
        
        try:
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                matches_list = []
                
                if 'matches' in data:
                    for match in data['matches']:
                        match_date_str = match.get('utcDate', '')[:10]
                        match_date = datetime.strptime(match_date_str, '%Y-%m-%d').date()
                        
                        # Φίλτρο: Μόνο σήμερα και αύριο
                        if match_date == today or match_date == tomorrow:
                            home = match.get('homeTeam', {}).get('name')
                            away = match.get('awayTeam', {}).get('name')
                            
                            if home and away:
                                tip = get_prediction_logic(home, away)
                                day_label = "Σήμερα" if match_date == today else "Αύριο"
                                matches_list.append(f"⚽ [{day_label}] {home} vs {away} -> {tip}")
                                found_any_match = True
                
                if matches_list:
                    all_content += f"--- {league_name} ---\n"
                    for m in matches_list:
                        all_content += m + "\n"
                    all_content += "\n"
            
            # Μικρή παύση 2 δευτερολέπτων για να μην μας μπλοκάρει το API (Limit 10 calls/min)
            time.sleep(2)
            
        except Exception as e:
            print(f"Σφάλμα στο πρωτάθλημα {league_name}: {e}")

    # Αποθήκευση
    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        if found_any_match:
            f.write(all_content)
        else:
            f.write(f"📅 {today.strftime('%d/%m')}\nΔεν βρέθηκαν αγώνες για σήμερα ή αύριο στα επιλεγμένα πρωταθλήματα.")

if __name__ == "__main__":
    get_predictions()

