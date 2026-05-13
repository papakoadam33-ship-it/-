import requests
import math
import time
from datetime import datetime

API_KEY = "a963742bcd5642afbe8c842d057f25ad"
HEADERS = { "X-Auth-Token": API_KEY }

def get_league_stats(league_code):
    """Τραβάει τη βαθμολογία και υπολογίζει attack/defense strength για κάθε ομάδα"""
    url = f"https://api.football-data.org/v4/competitions/{league_code}/standings"
    stats = {}
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        data = response.json()
        if 'standings' in data:
            # Παίρνουμε το 'table' από το συνολικό standing (index 0)
            table = data['standings'][0]['table']
            for team in table:
                team_name = team['team']['name']
                stats[team_name] = {
                    'played': team['playedGames'],
                    'scored': team['goalsFor'],
                    'conceded': team['goalsAgainst'],
                    'avg_scored': team['goalsFor'] / team['playedGames'] if team['playedGames'] > 0 else 0,
                    'avg_conceded': team['goalsAgainst'] / team['playedGames'] if team['playedGames'] > 0 else 0
                }
        return stats
    except Exception as e:
        print(f"Error fetching stats for {league_code}: {e}")
        return {}

def poisson_probability(lmbda, k):
    if lmbda <= 0: return 0
    return (math.exp(-lmbda) * (lmbda**k)) / math.factorial(k)

def calculate_tips(home_name, away_name, league_stats):
    """Υπολογίζει tips βασισμένα σε πραγματικά νούμερα"""
    # Αν δεν έχουμε στατιστικά, επιστρέφουμε ένα default
    if home_name not in league_stats or away_name not in league_stats:
        return "No Data", "No Data"

    h = league_stats[home_name]
    a = league_stats[away_name]

    # Υπολογισμός Lambda (Αναμενόμενα Γκολ)
    # Η λογική: Επίθεση γηπεδούχου x Άμυνα φιλοξενούμενου
    lmbda_h = h['avg_scored'] * (a['avg_conceded'] / 1.3) # 1.3 είναι ένας μέσος όρος γκολ
    lmbda_a = a['avg_scored'] * (h['avg_conceded'] / 1.3)
    lmbda_total = lmbda_h + lmbda_a

    # Πιθανότητες
    p0 = poisson_probability(lmbda_total, 0)
    p1 = poisson_probability(lmbda_total, 1)
    p2 = poisson_probability(lmbda_total, 2)
    
    prob_over_2_5 = (1 - (p0 + p1 + p2)) * 100
    prob_gg = (1 - poisson_probability(lmbda_h, 0)) * (1 - poisson_probability(lmbda_a, 0)) * 100

    # formatting tips
    if prob_over_2_5 > 55:
        return f"Over 2.5 ({int(prob_over_2_5)}%)", f"GG ({int(prob_gg)}%)"
    else:
        return f"Under 3.5 ({int(100-prob_over_2_5)}%)", f"1X ({int(60)}%)"

def fetch_data():
    # Λίστα με τα Codes των πρωταθλημάτων που υποστηρίζει το free tier
    leagues = {
        "PL": "🏴󠁧󠁢󠁥󠁮󠁧󠁿 PREMIER LEAGUE",
        "PD": "🇪🇸 LA LIGA",
        "SA": "🇮🇹 SERIE A",
        "BL1": "🇩🇪 BUNDESLIGA",
        "FL1": "🇫🇷 LIGUE 1"
    }

    all_predictions = []

    for code, label in leagues.items():
        print(f"Ανάλυση: {label}...")
        
        # 1. Παίρνουμε στατιστικά για τη λίγκα
        league_stats = get_league_stats(code)
        time.sleep(1.5) # Delay για το rate limit του API

        # 2. Παίρνουμε τους αγώνες της λίγκας
        url = f"https://api.football-data.org/v4/competitions/{code}/matches?status=SCHEDULED"
        response = requests.get(url, headers=HEADERS)
        matches_data = response.json()

        if 'matches' in matches_data:
            for m in matches_data['matches'][:10]: # Τα επόμενα 10 ματς
                home = m['homeTeam']['name']
                away = m['awayTeam']['name']
                
                tip1, tip2 = calculate_tips(home, away, league_stats)
                
                dt_obj = datetime.strptime(m['utcDate'], "%Y-%m-%dT%H:%M:%SZ")
                m_time = f"{(dt_obj.hour + 3) % 24:02d}:{dt_obj.minute:02d}"
                
                all_predictions.append(f"{label}|{home} - {away}|{m_time}|{tip1}|{tip2}")
        
        time.sleep(1.5) # Delay για το επόμενο request

    # Αποθήκευση
    with open("smart_predictions.txt", "w", encoding="utf-8") as f:
        for p in all_predictions:
            f.write(p + "\n")
    print("Done! Check smart_predictions.txt")

if __name__ == "__main__":
    fetch_data()
