import requests
import math
import time
from datetime import datetime, timezone, timedelta

# --- ΡΥΘΜΙΣΕΙΣ (Όλες οι επίσημες δωρεάν λίγκες του API σου) ---
API_KEY = "a963742bcd5642afbe8c842d057f25ad"
HEADERS = { "X-Auth-Token": API_KEY }

LEAGUES = {
    "PL": "PREMIER LEAGUE",
    "PD": "LA LIGA",
    "SA": "SERIE A",
    "BL1": "BUNDESLIGA",
    "FL1": "LIGUE 1",
    "DED": "EREDIVISIE",       # Ολλανδία (Νέο)
    "PPL": "PRIMEIRA LIGA",     # Πορτογαλία (Νέο)
    "ELC": "CHAMPIONSHIP"       # Β' Αγγλίας (Νέο)
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
        
        home_goals_total, home_games_total = 0, 0
        away_goals_total, away_games_total = 0, 0
        
        if st_res.status_code == 200:
            data = st_res.json()
            
            for standing in data.get('standings', []):
                st_type = standing.get('type') 
                
                for team in standing.get('table', []):
                    name = team['team']['name']
                    if name not in stats:
                        stats[name] = {
                            'home_avg_scored': 1.0, 'home_avg_conceded': 1.0,
                            'away_avg_scored': 1.0, 'away_avg_conceded': 1.0,
                            'recent_goals_scored': [], 'recent_goals_conceded': []
                        }
                    
                    games = team['playedGames']
                    if games > 0:
                        if st_type == 'HOME':
                            stats[name]['home_avg_scored'] = team['goalsFor'] / games
                            stats[name]['home_avg_conceded'] = team['goalsAgainst'] / games
                            home_goals_total += team['goalsFor']
                            home_games_total += games
                        elif st_type == 'AWAY':
                            stats[name]['away_avg_scored'] = team['goalsFor'] / games
                            stats[name]['away_avg_conceded'] = team['goalsAgainst'] / games
                            away_goals_total += team['goalsFor']
                            away_games_total += games

            league_home_avg = (home_goals_total / home_games_total) if home_games_total > 0 else 1.5
            league_away_avg = (away_goals_total / away_games_total) if away_games_total > 0 else 1.2
            
            for team in stats:
                stats[team]['league_home_avg'] = league_home_avg
                stats[team]['league_away_avg'] = league_away_avg

        time.sleep(6) 

        m_res = requests.get(matches_url, headers=HEADERS, timeout=15)
        if m_res.status_code == 200:
            all_matches = m_res.json().get('matches', [])
            for match in reversed(all_matches):
                h_team, a_team = match['homeTeam']['name'], match['awayTeam']['name']
                
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
        print(f"Error fetching stats for {league_code}: {e}")
        return {}

def calculate_prediction(home, away, league_stats):
    if home not in league_stats or away not in league_stats:
        return "N/A", 0, "N/A"

    h_s, a_s = league_stats[home], league_stats[away]
    
    lg_home_avg = h_s['league_home_avg']
    lg_away_avg = h_s['league_away_avg']
    
    def get_weighted_val(recent, overall_specific):
        r_avg = sum(recent)/len(recent) if recent else overall_specific
        return (r_avg * 0.7) + (overall_specific * 0.3)

    home_attack = get_weighted_val(h_s['recent_goals_scored'], h_s['home_avg_scored'])
    away_defense = get_weighted_val(a_s['recent_goals_conceded'], a_s['away_avg_conceded'])
    
    away_attack = get_weighted_val(a_s['recent_goals_scored'], a_s['away_avg_scored'])
    home_defense = get_weighted_val(h_s['recent_goals_conceded'], h_s['home_avg_conceded'])

    l_h = (home_attack / lg_home_avg) * (away_defense / lg_away_avg) * lg_home_avg
    l_a = (away_attack / lg_away_avg) * (home_defense / lg_home_avg) * lg_away_avg
    l_total = l_h + l_a

    prob_under_2_5 = sum(poisson_probability(l_total, k) for k in range(3))
    prob_over = (1 - prob_under_2_5) * 100
    prob_2_3 = (poisson_probability(l_total, 2) + poisson_probability(l_total, 3)) * 100
    prob_gg = (1 - poisson_probability(l_h, 0)) * (1 - poisson_probability(l_a, 0)) * 100

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
    # Ώρα Ελλάδας (UTC+3)
    now_gr = datetime.now(timezone.utc) + timedelta(hours=3)
    today_str = now_gr.strftime("%Y-%m-%d")
    
    print(f"Starting advanced predictions for: {today_str}")
    
    for code, label in LEAGUES.items():
        print(f"Processing {label}...")
        l_stats = get_advanced_stats(code)
        if not l_stats:
            continue
        time.sleep(6)

        url = f"https://api.football-data.org/v4/competitions/{code}/matches"
        try:
            res = requests.get(url, headers=HEADERS).json()
            for m in res.get('matches', []):
                if m['status'] in ['SCHEDULED', 'TIMED']:
                    utc_dt = datetime.strptime(m['utcDate'], "%Y-%m-%dT%H:%M:%SZ")
                    gr_dt = utc_dt.replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=3)))
                    match_date_str = gr_dt.strftime("%Y-%m-%d")
                    
                    if match_date_str == today_str:
                        home, away = m['homeTeam']['name'], m['awayTeam']['name']
                        tip, pct, cover = calculate_prediction(home, away, l_stats)
                        
                        if tip == "N/A": 
                            continue
                            
                        m_time = gr_dt.strftime("%d/%m %H:%M")
                        predictions.append(f"{label}|{home} - {away}|{m_time}|{tip}|{pct}|{cover}")
        except Exception as e:
            print(f"Error parsing matches for {code}: {e}")
            continue
        time.sleep(6)

    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        timestamp = now_gr.strftime("%d/%m/%Y %H:%M")
        f.write(f"--- ΠΡΟΓΝΩΣΤΙΚΑ {timestamp} ---\n")
        f.write("ΛΙΓΚΑ|ΑΓΩΝΑΣ|ΩΡΑ|ΠΡΟΒΛΕΨΗ|ΠΟΣΟΣΤΟ|ΚΑΛΥΨΗ\n")
        
        if not predictions:
            f.write("INFO|Δεν υπάρχουν σημερινοί αγώνες.|-| - | 0 | - \n")
            print("No matches found for today.")
        else:
            for p in predictions:
                f.write(p + "\n")
            print(f"Successfully generated {len(predictions)} predictions!")

if __name__ == "__main__":
    main()
