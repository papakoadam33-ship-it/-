import requests
import math
import time
from datetime import datetime, timedelta

# --- ΡΥΘΜΙΣΕΙΣ ---
API_KEY = "a963742bcd5642afbe8c842d057f25ad"
HEADERS = { "X-Auth-Token": API_KEY }

LEAGUES = {
    "PL": "PREMIER LEAGUE",
    "PD": "LA LIGA",
    "SA": "SERIE A",
    "BL1": "BUNDESLIGA",
    "FL1": "LIGUE 1",
    "WC": "WORLD CUP"
}

def poisson_probability(lmbda, k):
    if lmbda <= 0: return 0
    return (math.exp(-lmbda) * (lmbda**k)) / math.factorial(k)

def get_advanced_stats(league_code):
    stats = {}
    standings_url = f"https://api.football-data.org/v4/competitions/{league_code}/standings"
    matches_url = f"https://api.football-data.org/v4/competitions/{league_code}/matches?status=FINISHED"

    try:
        st_res = requests.get(standings_url, headers=HEADERS, timeout=15)
        if st_res.status_code == 200:
            data = st_res.json()
            for standing in data.get('standings', []):
                for team in standing.get('table', []):
                    name = team['team']['name']
                    stats[name] = {
                        'overall_avg_scored': team['goalsFor'] / team['playedGames'] if team['playedGames'] > 0 else 1.0,
                        'overall_avg_conceded': team['goalsAgainst'] / team['playedGames'] if team['playedGames'] > 0 else 1.0,
                        'recent_goals_scored': [],
                        'recent_goals_conceded': []
                    }

        time.sleep(6)

        m_res = requests.get(matches_url, headers=HEADERS, timeout=15)
        if m_res.status_code == 200:
            for match in reversed(m_res.json().get('matches', [])[-60:]):
                h_team, a_team = match['homeTeam']['name'], match['awayTeam']['name']
                if match['score']['fullTime']['home'] is not None:
                    h_score = match['score']['fullTime']['home']
                    a_score = match['score']['fullTime']['away']

                    if h_team in stats and len(stats[h_team]['recent_goals_scored']) < 5:
                        stats[h_team]['recent_goals_scored'].append(h_score)
                        stats[h_team]['recent_goals_conceded'].append(a_score)
                    if a_team in stats and len(stats[a_team]['recent_goals_scored']) < 5:
                        stats[a_team]['recent_goals_scored'].append(a_score)
                        stats[a_team]['recent_goals_conceded'].append(h_score)
        return stats
    except:
        return {}

def calculate_prediction(home, away, league_stats):
    if home not in league_stats or away not in league_stats:
        return "2-3 Goals", 55, "GG (58%)"

    h_s, a_s = league_stats[home], league_stats[away]
    
    def get_val(recent, overall):
        r_avg = sum(recent)/len(recent) if recent else overall
        return (r_avg * 0.7) + (overall * 0.3)

    l_h = get_val(h_s['recent_goals_scored'], h_s['overall_avg_scored']) * (get_val(a_s['recent_goals_conceded'], a_s['overall_avg_conceded']) / 1.3)
    l_a = get_val(a_s['recent_goals_scored'], a_s['overall_avg_scored']) * (get_val(h_s['recent_goals_conceded'], h_s['overall_avg_conceded']) / 1.3)
    l_total = l_h + l_a

    prob_under_2_5 = sum(poisson_probability(l_total, k) for k in range(3))
    prob_over = (1 - prob_under_2_5) * 100
    prob_2_3 = (poisson_probability(l_total, 2) + poisson_probability(l_total, 3)) * 100
    prob_gg = (1 - poisson_probability(l_h, 0)) * (1 - poisson_probability(l_a, 0)) * 100

    # Δυναμική επιλογή σημείου με βάση το μεγαλύτερο ποσοστό
    if prob_over > 60:
        tip = "Over 2.5"
        pct = int(prob_over)
    elif prob_over < 40:
        tip = "Under 2.5"
        pct = int(100 - prob_over)
    else:
        tip = "2-3 Goals"
        pct = int(prob_2_3 if prob_2_3 > 45 else 55)

    cover = f"GG ({int(prob_gg)}%)" if prob_gg > 50 else f"No GG ({int(100-prob_gg)}%)"
    return tip, pct, cover

def main():
    predictions = []
    now_gr = datetime.utcnow() + timedelta(hours=3)
    today_str = now_gr.strftime("%Y-%m-%d")
    
    for code, label in LEAGUES.items():
        l_stats = get_advanced_stats(code)
        time.sleep(6)

        url = f"https://api.football-data.org/v4/competitions/{code}/matches"
        try:
            res = requests.get(url, headers=HEADERS).json()
            for m in res.get('matches', []):
                if m['status'] in ['SCHEDULED', 'TIMED']:
                    utc_dt = datetime.strptime(m['utcDate'], "%Y-%m-%dT%H:%M:%SZ")
                    gr_dt = utc_dt + timedelta(hours=3)
                    match_date_str = gr_dt.strftime("%Y-%m-%d")
                    
                    if match_date_str == today_str:
                        home, away = m['homeTeam']['name'], m['awayTeam']['name']
                        tip, pct, cover = calculate_prediction(home, away, l_stats)
                        m_time = gr_dt.strftime("%d/%m %H:%M")
                        # Αποθηκεύουμε και το ποσοστό (pct) ξεχωριστά
                        predictions.append(f"{label}|{home} - {away}|{m_time}|{tip}|{pct}|{cover}")
        except:
            continue
        time.sleep(6)

    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        timestamp = now_gr.strftime("%d/%m/%Y %H:%M")
        f.write(f"--- ΠΡΟΓΝΩΣΤΙΚΑ {timestamp} ---\n")
        f.write("ΛΙΓΚΑ|ΑΓΩΝΑΣ|ΩΡΑ|ΠΡΟΒΛΕΨΗ|ΠΟΣΟΣΤΟ|ΚΑΛΥΨΗ\n")
        
        if not predictions:
            f.write("INFO|Δεν υπάρχουν σημερινοί αγώνες.|-| - | 0 | - \n")
        else:
            for p in predictions:
                f.write(p + "\n")

if __name__ == "__main__":
    main()
