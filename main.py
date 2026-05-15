import requests
import math
import time
from datetime import datetime, timedelta

# --- ΡΥΘΜΙΣΕΙΣ ---
API_KEY = "a963742bcd5642afbe8c842d057f25ad"
HEADERS = { "X-Auth-Token": API_KEY }

# Λίστα με τα Codes των πρωταθλημάτων (Free Tier)
LEAGUES = {
    "PL": "PREMIER LEAGUE",
    "PD": "LA LIGA",
    "SA": "SERIE A",
    "BL1": "BUNDESLIGA",
    "FL1": "LIGUE 1"
}

def poisson_probability(lmbda, k):
    if lmbda <= 0: return 0
    return (math.exp(-lmbda) * (lmbda**k)) / math.factorial(k)

def get_advanced_stats(league_code):
    stats = {}
    standings_url = f"https://api.football-data.org/v4/competitions/{league_code}/standings"
    matches_url = f"https://api.football-data.org/v4/competitions/{league_code}/matches?status=FINISHED"

    try:
        # 1. Βαθμολογία
        st_res = requests.get(standings_url, headers=HEADERS, timeout=15)
        if st_res.status_code == 200:
            for team in st_res.json()['standings'][0]['table']:
                name = team['team']['name']
                stats[name] = {
                    'overall_avg_scored': team['goalsFor'] / team['playedGames'],
                    'overall_avg_conceded': team['goalsAgainst'] / team['playedGames'],
                    'recent_goals_scored': [],
                    'recent_goals_conceded': []
                }

        # 2. Φόρμα τελευταίων 5 αγώνων
        m_res = requests.get(matches_url, headers=HEADERS, timeout=15)
        if m_res.status_code == 200:
            for match in reversed(m_res.json()['matches'][-120:]):
                h_team, a_team = match['homeTeam']['name'], match['awayTeam']['name']
                h_score, a_score = match['score']['fullTime']['home'], match['score']['fullTime']['away']

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
        return "N/A (0%)", "N/A (0%)"

    h_s, a_s = league_stats[home], league_stats[away]
    
    def get_val(recent, overall):
        r_avg = sum(recent)/len(recent) if recent else overall
        return (r_avg * 0.7) + (overall * 0.3)

    l_h = get_val(h_s['recent_goals_scored'], h_s['overall_avg_scored']) * (get_val(a_s['recent_goals_conceded'], a_s['overall_avg_conceded']) / 1.3)
    l_a = get_val(a_s['recent_goals_scored'], a_s['overall_avg_scored']) * (get_val(h_s['recent_goals_conceded'], h_s['overall_avg_conceded']) / 1.3)
    l_total = l_h + l_a

    # Υπολογισμός Over 2.5
    prob_under_2_5 = sum(poisson_probability(l_total, k) for k in range(3))
    prob_over = (1 - prob_under_2_5) * 100
    
    # Υπολογισμός GG
    prob_gg = (1 - poisson_probability(l_h, 0)) * (1 - poisson_probability(l_a, 0)) * 100

    # Κύριο Tip
    if prob_over > 60: tip = f"Over 2.5 ({int(prob_over)}%)"
    elif prob_over < 40: tip = f"Under 2.5 ({int(100-prob_over)}%)"
    else: tip = f"2-3 Goals ({int(55)}%)"

    # Κάλυψη
    cover_label = "GG" if prob_gg > 50 else "No GG"
    cover_pct = int(prob_gg) if prob_gg > 50 else int(100 - prob_gg)
    cover = f"{cover_label} ({cover_pct}%)"
    
    return tip, cover

def main():
    predictions = []
    # Ώρα Ελλάδας τώρα
    now_gr = datetime.utcnow() + timedelta(hours=3)
    today_str = now_gr.strftime("%Y-%m-%d")
    
    for code, label in LEAGUES.items():
        l_stats = get_advanced_stats(code)
        time.sleep(2) 

        url = f"https://api.football-data.org/v4/competitions/{code}/matches?status=SCHEDULED"
        try:
            res = requests.get(url, headers=HEADERS).json()
            for m in res.get('matches', []):
                # Μετατροπή UTC σε Ελλάδα για το φιλτράρισμα
                utc_dt = datetime.strptime(m['utcDate'], "%Y-%m-%dT%H:%M:%SZ")
                gr_dt = utc_dt + timedelta(hours=3)
                
                # ΦΙΛΤΡΟ: Μόνο για τη σημερινή ημερομηνία (βάσει ώρας Ελλάδας)
                if gr_dt.strftime("%Y-%m-%d") == today_str:
                    home, away = m['homeTeam']['name'], m['awayTeam']['name']
                    tip, cover = calculate_prediction(home, away, l_stats)
                    
                    m_time = gr_dt.strftime("%H:%M")
                    predictions.append(f"{label}|{home} - {away}|{m_time}|{tip}|{cover}")
        except:
            continue
        time.sleep(2)

    # Εγγραφή στο αρχείο για το Streamlit
    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        timestamp = now_gr.strftime("%d/%m/%Y %H:%M")
        f.write(f"--- ΠΡΟΓΝΩΣΤΙΚΑ {timestamp} ---\n")
        f.write("ΛΙΓΚΑ|ΑΓΩΝΑΣ|ΩΡΑ|ΠΡΟΒΛΕΨΗ|ΚΑΛΥΨΗ\n")
        
        if not predictions:
            f.write("INFO|Δεν υπάρχουν αγώνες για σήμερα.|-| - | - \n")
        else:
            for p in predictions:
                f.write(p + "\n")

if __name__ == "__main__":
    main()

