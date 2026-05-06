import requests
import time
from datetime import datetime, timedelta

# Βάλε το κλειδί σου εδώ
API_KEY = "a1a4edf072dc4b2c8153fced44c88de9"

# Επιλεγμένα πρωταθλήματα (Free Tier)
LEAGUES = {
    'Premier League': 'PL',
    'La Liga': 'PD',
    'Serie A': 'SA',
    'Bundesliga': 'BL1',
    'Ligue 1': 'FL1',
    'Brazil Serie A': 'BSA',
    'Portugal Primeira Liga': 'PPL'
}

def get_smart_prediction(home_rank, away_rank):
    """Λογική βασισμένη στη θέση στη βαθμολογία"""
    if home_rank and away_rank:
        diff = home_rank - away_rank
        if diff < -8: return "1 & Over 1.5"
        if diff > 8: return "X2 & Over 1.5"
        if abs(diff) <= 4: return "Goal-Goal"
    return "Over 1.5"

def get_predictions():
    clean_key = str(API_KEY).strip()
    headers = { 'X-Auth-Token': clean_key }
    
    today = datetime.utcnow().date()
    tomorrow = today + timedelta(days=1)
    
    all_content = f"📅 Προγνωστικά: {today.strftime('%d/%m')} & {tomorrow.strftime('%d/%m')}\n\n"
    found_any_match = False

    for league_name, league_code in LEAGUES.items():
        try:
            print(f"Fetching {league_name}...")
            
            # 1. Λήψη Βαθμολογίας
            standings_url = f"https://api.football-data.org/v4/competitions/{league_code}/standings"
            st_res = requests.get(standings_url, headers=headers)
            ranks = {}
            if st_res.status_code == 200:
                data_st = st_res.json()
                for table in data_st.get('standings', [{}])[0].get('table', []):
                    team_name = table['team']['name']
                    ranks[team_name] = table['position']
            
            # Μεγάλη παύση για να μην φάμε block (6 δευτερόλεπτα)
            time.sleep(6)

            # 2. Λήψη Αγώνων
            matches_url = f"https://api.football-data.org/v4/competitions/{league_code}/matches?status=SCHEDULED"
            m_res = requests.get(matches_url, headers=headers)
            
            if m_res.status_code == 200:
                matches_data = m_res.json()
                league_has_matches = False
                temp_matches = ""
                
                for match in matches_data.get('matches', []):
                    m_date_str = match.get('utcDate', '')[:10]
                    m_date = datetime.strptime(m_date_str, '%Y-%m-%d').date()
                    
                    if m_date == today or m_date == tomorrow:
                        h_team = match['homeTeam']['name']
                        a_team = match['awayTeam']['name']
                        h_rank = ranks.get(h_team)
                        a_rank = ranks.get(a_team)
                        
                        tip = get_smart_prediction(h_rank, a_rank)
                        day_label = "Σήμερα" if m_date == today else "Αύριο"
                        
                        temp_matches += f"⚽ [{day_label}] {h_team} vs {a_team} -> {tip}\n"
                        league_has_matches = True
                        found_any_match = True
                
                if league_has_matches:
                    all_content += f"--- {league_name} ---\n" + temp_matches + "\n"
            
            # Άλλη μια παύση πριν το επόμενο πρωτάθλημα
            time.sleep(6)
            
        except Exception as e:
            print(f"Error in {league_name}: {e}")

    # Τελική εγγραφή
    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        if found_any_match:
            f.write(all_content)
        else:
            f.write(f"📅 {today.strftime('%d/%m')}\nΔεν βρέθηκαν αγώνες για σήμερα ή αύριο.")

if __name__ == "__main__":
    get_predictions()

