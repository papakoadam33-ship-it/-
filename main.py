import requests
import time
from datetime import datetime, timedelta

API_KEY = "ΤΟ_ΚΛΕΙΔΙ_ΣΟΥ_ΕΔΩ"

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
    """Λογική βασισμένη στη θέση της ομάδας στη βαθμολογία"""
    if home_rank and away_rank:
        diff = home_rank - away_rank
        # Αν η γηπεδούχος είναι πολύ καλύτερη (π.χ. 1η vs 15η)
        if diff < -10: return "1 & Over 1.5"
        # Αν η φιλοξενούμενη είναι πολύ καλύτερη
        if diff > 10: return "X2 & Over 1.5"
        # Αν είναι κοντά στη βαθμολογία
        if abs(diff) <= 3: return "Goal-Goal"
    
    return "Over 1.5"

def get_predictions():
    clean_key = str(API_KEY).strip()
    headers = { 'X-Auth-Token': clean_key }
    today = datetime.utcnow().date()
    tomorrow = today + timedelta(days=1)
    all_content = f"📅 Προγνωστικά: {today.strftime('%d/%m')} & {tomorrow.strftime('%d/%m')}\n\n"

    for league_name, league_code in LEAGUES.items():
        try:
            # 1. Παίρνουμε τη βαθμολογία (Standings) για να ξέρουμε ποιος είναι καλός
            standings_url = f"https://api.football-data.org/v4/competitions/{league_code}/standings"
            st_res = requests.get(standings_url, headers=headers)
            ranks = {}
            if st_res.status_code == 200:
                data_st = st_res.json()
                for table in data_st.get('standings', [{}])[0].get('table', []):
                    ranks[table['team']['name']] = table['position']

            time.sleep(2) # Delay για το API limit

            # 2. Παίρνουμε τους αγώνες
            matches_url = f"https://api.football-data.org/v4/competitions/{league_code}/matches?status=SCHEDULED"
            m_res = requests.get(matches_url, headers=headers)
            if m_res.status_code == 200:
                matches_data = m_res.json()
                matches_list = []
                for match in matches_data.get('matches', []):
                    m_date = datetime.strptime(match['utcDate'][:10], '%Y-%m-%d').date()
                    if m_date == today or m_date == tomorrow:
                        h_team = match['homeTeam']['name']
                        a_team = match['awayTeam']['name']
                        h_rank = ranks.get(h_team)
                        a_rank = ranks.get(a_team)
                        
                        tip = get_smart_prediction(h_rank, a_rank)
                        day = "Σήμερα" if m_date == today else "Αύριο"
                        matches_list.append(f"⚽ [{day}] {h_team} vs {a_team} -> {tip}")

                if matches_list:
                    all_content += f"--- {league_name} ---\n" + "\n".join(matches_list) + "\n\n"
            
            time.sleep(2)
        except Exception as e:
            print(f"Error in {league_name}: {e}")

    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        f.write(all_content)

if __name__ == "__main__":
    get_predictions()

