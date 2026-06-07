import requests
import math
import time
from datetime import datetime, timedelta, timezone

# --- ΡΥΘΜΙΣΕΙΣ ---
API_KEY = "a963742bcd5642afbe8c842d057f25ad"
HEADERS = { "X-Auth-Token": API_KEY }

# Προστέθηκε η Βραζιλία (BSA) που έχει αγώνες το καλοκαίρι
LEAGUES = {
    "BSA": "Campeonato Brasileiro",
    "PL": "Premier League",
    "PD": "La Liga",
    "SA": "Serie A",
    "BL1": "Bundesliga",
    "FL1": "Ligue 1",
    "CL": "Champions League",
    "EC": "Euro",
    "WC": "World Cup"
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
        
        time.sleep(7)

        m_res = requests.get(matches_url, headers=HEADERS, timeout=15)
        if m_res.status_code == 200:
            all_matches = m_res.json().get('matches', [])
            for match in reversed(all_matches[-80:]):
                h_team = match['homeTeam']['name']
                a_team = match['awayTeam']['name']
                
                if match.get('score', {}).get('fullTime', {}).get('home') is not None:
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
        print(f"Σφάλμα στατιστικών {league_code}: {e}")
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

    if prob_over > 58:
        tip = "Over 2.5"
        pct = int(prob_over)
    elif prob_over < 42:
        tip = "Under 2.5"
        pct = int(100 - prob_over)
    else:
        tip = "2-3 Goals"
        pct = int(prob_2_3 if prob_2_3 > 45 else 55)

    cover = f"GG ({int(prob_gg)}%)" if prob_gg > 50 else f"No GG ({int(100-prob_gg)}%)"
    return tip, pct, cover

def main():
    predictions = []
    # Χρήση timezone-aware UTC+3 για την Ελλάδα
    now_gr = datetime.now(timezone.utc) + timedelta(hours=3)
    
    # Φτιάχνει λίστα με τις επόμενες 7 ημέρες για να τραβάει αρκετούς αγώνες
    allowed_dates = [(now_gr.date() + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
    
    for code, label in LEAGUES.items():
        l_stats = get_advanced_stats(code)
        time.sleep(7)

        url = f"https://api.football-data.org/v4/competitions/{code}/matches"
        try:
            res = requests.get(url, headers=HEADERS, timeout=15)
            if res.status_code == 200:
                matches_data = res.json()
                for m in matches_data.get('matches', []):
                    if m['status'] in ['SCHEDULED', 'TIMED']:
                        # Μετατροπή της ώρας σε UTC+3
                        utc_dt = datetime.fromisoformat(m['utcDate'].replace("Z", "+00:00"))
                        gr_dt = utc_dt + timedelta(hours=3)
                        match_date_str = gr_dt.strftime("%Y-%m-%d")
                        
                        # Έλεγχος αν ο αγώνας είναι μέσα στο επόμενο 7ήμερο
                        if match_date_str in allowed_dates:
                            home = m['homeTeam']['name']
                            away = m['awayTeam']['name']
                            tip, pct, cover = calculate_prediction(home, away, l_stats)
                            m_time = gr_dt.strftime("%d/%m %H:%M") # Εμφανίζει και την ημερομηνία
                            predictions.append(f"{label}|{home} - {away}|{m_time}|{tip}|{pct}|{cover}")
        except Exception as e:
            continue
        
        time.sleep(7)

    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        timestamp = now_gr.strftime("%d/%m/%Y %H:%M")
        f.write(f"--- ΠΡΟΓΝΩΣΤΙΚΑ {timestamp} ---\n")
        f.write("ΛΙΓΚΑ|ΑΓΩΝΑΣ|ΗΜΕΡ_ΩΡΑ|ΠΡΟΒΛΕΨΗ|ΠΟΣΟΣΤΟ|ΚΑΛΥΨΗ\n")
        for p in predictions:
            f.write(p + "\n")

if __name__ == "__main__":
    main()

