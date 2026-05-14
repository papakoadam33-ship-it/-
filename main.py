import requests
import math
import time
from datetime import datetime, timedelta

# --- ΡΥΘΜΙΣΕΙΣ ---
API_KEY = "a963742bcd5642afbe8c842d057f25ad"
HEADERS = { "X-Auth-Token": API_KEY }

# Ενημερωμένη λίστα πρωταθλημάτων
LEAGUES = {
    "PL": "PREMIER LEAGUE",
    "PD": "LA LIGA",
    "SA": "SERIE A",
    "BL1": "BUNDESLIGA",
    "FL1": "LIGUE 1",
    "ELC": "CHAMPIONSHIP",
    "DED": "EREDIVISIE",
    "PPL": "PRIMEIRA LIGA",
    "BSA": "BRAZIL SERIE A",
    "CL": "CHAMPIONS LEAGUE"
}

def poisson_probability(lmbda, k):
    """Υπολογίζει την πιθανότητα Poisson για k γκολ"""
    if lmbda <= 0: return 0
    return (math.exp(-lmbda) * (lmbda**k)) / math.factorial(k)

def get_advanced_stats(league_code):
    """Τραβάει στατιστικά σεζόν και φόρμα τελευταίων αγώνων"""
    stats = {}
    standings_url = f"https://api.football-data.org/v4/competitions/{league_code}/standings"
    matches_url = f"https://api.football-data.org/v4/competitions/{league_code}/matches?status=FINISHED"

    try:
        # 1. Βαθμολογία
        st_res = requests.get(standings_url, headers=HEADERS, timeout=15)
        if st_res.status_code == 200:
            data = st_res.json()
            if 'standings' in data and data['standings']:
                for team in data['standings'][0]['table']:
                    name = team['team']['name']
                    games = team['playedGames'] if team['playedGames'] > 0 else 1
                    stats[name] = {
                        'overall_avg_scored': team['goalsFor'] / games,
                        'overall_avg_conceded': team['goalsAgainst'] / games,
                        'recent_goals_scored': [],
                        'recent_goals_conceded': []
                    }

        # 2. Φόρμα (Τελευταία 80 ματς για οικονομία στο API)
        m_res = requests.get(matches_url, headers=HEADERS, timeout=15)
        if m_res.status_code == 200:
            matches_data = m_res.json().get('matches', [])
            for match in reversed(matches_data[-80:]):
                h_team, a_team = match['homeTeam']['name'], match['awayTeam']['name']
                h_score = match['score']['fullTime']['home']
                a_score = match['score']['fullTime']['away']

                if h_team in stats and len(stats[h_team]['recent_goals_scored']) < 5:
                    stats[h_team]['recent_goals_scored'].append(h_score)
                    stats[h_team]['recent_goals_conceded'].append(a_score)
                if a_team in stats and len(stats[a_team]['recent_goals_scored']) < 5:
                    stats[a_team]['recent_goals_scored'].append(a_score)
                    stats[a_team]['recent_goals_conceded'].append(h_score)
        return stats
    except Exception as e:
        print(f"Error fetching stats for {league_code}: {e}")
        return {}

def calculate_prediction(home, away, league_stats):
    """Κύριος αλγόριθμος πρόβλεψης Poisson"""
    if home not in league_stats or away not in league_stats:
        return "1X & Over 1.5 (72%)", "Goal-Goal (55%)"

    h_s, a_s = league_stats[home], league_stats[away]
    
    def get_val(recent, overall):
        r_avg = sum(recent)/len(recent) if recent else overall
        return (r_avg * 0.7) + (overall * 0.3)

    l_h = get_val(h_s['recent_goals_scored'], h_s['overall_avg_scored']) * (get_val(a_s['recent_goals_conceded'], a_s['overall_avg_conceded']) / 1.3)
    l_a = get_val(a_s['recent_goals_scored'], a_s['overall_avg_scored']) * (get_val(h_s['recent_goals_conceded'], h_s['overall_avg_conceded']) / 1.3)
    l_total = l_h + l_a

    prob_under_2_5 = sum(poisson_probability(l_total, k) for k in range(3))
    prob_over = (1 - prob_under_2_5) * 100
    prob_gg = (1 - poisson_probability(l_h, 0)) * (1 - poisson_probability(l_a, 0)) * 100

    # Κύριο Tip
    if prob_over > 60: tip = f"Over 2.5 ({int(prob_over)}%)"
    elif prob_over < 40: tip = f"Under 2.5 ({int(100-prob_over)}%)"
    else: tip = f"1X & Over 1.5 (75%)"

    # Κάλυψη
    if prob_gg > 52: cover = f"Goal-Goal ({int(prob_gg)}%)"
    else: cover = f"2-3 Goals (50%)"
    
    return tip, cover

def main():
    predictions = []
    now_gr = datetime.utcnow() + timedelta(hours=3)
    today_str = now_gr.strftime("%Y-%m-%d")
    
    for code, label in LEAGUES.items():
        print(f"📊 Επεξεργασία: {label}...")
        l_stats = get_advanced_stats(code)
        time.sleep(2) 

        url = f"https://api.football-data.org/v4/competitions/{code}/matches?status=SCHEDULED"
        try:
            res = requests.get(url, headers=HEADERS).json()
            for m in res.get('matches', []):
                match_date = m['utcDate'].split("T")[0]
                if match_date != today_str: continue

                home, away = m['homeTeam']['name'], m['awayTeam']['name']
                tip, cover = calculate_prediction(home, away, l_stats)
                
                utc_dt = datetime.strptime(m['utcDate'], "%Y-%m-%dT%H:%M:%SZ")
                gr_dt = utc_dt + timedelta(hours=3)
                m_time = gr_dt.strftime("%H:%M")
                
                predictions.append(f"{label}|{home} - {away}|{m_time}|{tip}|{cover}")
        except Exception as e:
            print(f"Σφάλμα στη λίγκα {label}: {e}")
        time.sleep(2)

    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        timestamp = now_gr.strftime("%d/%m/%Y %H:%M")
        f.write(f"ΗΜΕΡΟΜΗΝΙΑ|{now_gr.strftime('%d/%m/%Y')}|{now_gr.strftime('%H:%M')}\n")
        if not predictions:
            f.write("INFO|Δεν υπάρχουν αγώνες για σήμερα.|-| - | - \n")
        else:
            for p in predictions: f.write(p + "\n")
    print("✅ Ενημερώθηκε!")

if __name__ == "__main__":
    main()
