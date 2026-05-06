import requests
from datetime import datetime, timedelta

# Το κλειδί σου
API_KEY = "ΤΟ_ΚΛΕΙΔΙ_ΣΟΥ_ΕΔΩ"

LEAGUES = {
    'Premier League': 'PL',
    'La Liga': 'PD',
    'Serie A': 'SA',
    'Bundesliga': 'BL1',
    'Ligue 1': 'FL1',
    'Champions League': 'CL'
}

def get_prediction_logic(home_team, away_team):
    """Μια απλή λογική για ποικιλία στα προγνωστικά"""
    name_len = len(home_team) + len(away_team)
    if name_len % 3 == 0:
        return "Over 2.5"
    elif name_len % 3 == 1:
        return "Goal-Goal"
    else:
        return "1X & Over 1.5"

def get_predictions():
    clean_key = str(API_KEY).strip()
    headers = { 'X-Auth-Token': clean_key }
    
    # Ημερομηνίες: Σήμερα και Αύριο
    today = datetime.utcnow().date()
    tomorrow = today + timedelta(days=1)
    
    all_content = f"📅 Προγνωστικά: {today.strftime('%d/%m')} & {tomorrow.strftime('%d/%m')}\n\n"
    
    for league_name, league_code in LEAGUES.items():
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
                                # Παίρνουμε ένα τυχαίο/λογικό προγνωστικό
                                tip = get_prediction_logic(home, away)
                                day_label = "Σήμερα" if match_date == today else "Αύριο"
                                matches_list.append(f"⚽ [{day_label}] {home} vs {away} -> {tip}")
                
                if matches_list:
                    all_content += f"--- {league_name} ---\n"
                    for m in matches_list:
                        all_content += m + "\n"
                    all_content += "\n"
        except Exception as e:
            print(f"Error in {league_name}: {e}")

    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        f.write(all_content if "---" in all_content else "Δεν βρέθηκαν αγώνες για σήμερα ή αύριο.")

if __name__ == "__main__":
    get_predictions()

