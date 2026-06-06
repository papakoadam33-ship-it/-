import os
import requests
import math
import time
import sqlite3
from datetime import datetime, timedelta

# --- API KEYS (Διαβάζονται αυτόματα από τα GitHub Secrets) ---
FOOTBALL_KEY = os.environ.get("FOOTBALL_API_KEY", "a963742bcd5642afbe8c842d057f25ad")
ODDS_KEY = os.environ.get("ba7b6e1475e3deaf847ca17f0fb0fded")

HEADERS_FOOTBALL = { "X-Auth-Token": FOOTBALL_KEY }
BANKROLL = 1000.0  # Το κεφάλαιό σου για το Kelly Criterion

# Λίγκες και τα αντίστοιχα IDs τους για το Odds API
LEAGUES = {
    "PL": {"name": "Premier League", "odds_market": "soccer_epl"},
    "PD": {"name": "La Liga", "odds_market": "soccer_spain_la_liga"},
    "SA": {"name": "Serie A", "odds_market": "soccer_italy_serie_a"},
    "BL1": {"name": "Bundesliga", "odds_market": "soccer_germany_bundesliga"},
    "FL1": {"name": "Ligue 1", "odds_market": "soccer_france_ligue_one"},
    "CL": {"name": "Champions League", "odds_market": "soccer_uefa_champs_league"}
}

# --- DATABASE SETUP ---
def init_database():
    conn = sqlite3.connect("betting_history.db")
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT, league TEXT, home_team TEXT, away_team TEXT,
        prediction TEXT, confidence TEXT, exact_scores TEXT, odds REAL, stake REAL
    )
    ''')
    conn.commit()
    conn.close()

# --- FETCH REAL ODDS (The Odds API) ---
def get_real_odds(odds_market):
    odds_dict = {}
    if not ODDS_KEY or "YOUR_ODDS" in ODDS_KEY:
        return odds_dict

    url = f"https://api.the-odds-api.com/v4/sports/{odds_market}/odds/"
    params = {
        'apiKey': ODDS_KEY,
        'regions': 'eu',         # Ευρωπαϊκοί Μπουκ (Stoiximan, Bet365, κλπ)
        'markets': 'totals',     # Over/Under 2.5
        'oddsFormat': 'decimal'
    }
    try:
        res = requests.get(url, params=params, timeout=15)
        if res.status_code == 200:
            data = res.json()
            for match in data:
                home = match['home_team']
                away = match['away_team']
                match_key = f"{home}-{away}"
                
                # Επιλογή του πρώτου διαθέσιμου Bookmaker
                if match.get('bookmakers'):
                    bookmaker = match['bookmakers'][0] 
                    for market in bookmaker.get('markets', []):
                        if market['key'] == 'totals':
                            for outcome in market['outcomes']:
                                if outcome.get('point') == 2.5:
                                    if match_key not in odds_dict:
                                        odds_dict[match_key] = {}
                                    odds_dict[match_key][outcome['name']] = outcome['price']
    except Exception as e:
        print(f"Σφάλμα στο Odds API ({odds_market}): {e}")
    return odds_dict

# --- ΜΑΘΗΜΑΤΙΚΑ POISSON & KELLY ---
def poisson_probability(lmbda, k):
    if lmbda <= 0: return 0
    return (math.exp(-lmbda) * (lmbda**k)) / math.factorial(k)

def confidence_stars(pct):
    if pct >= 85: return "⭐⭐⭐⭐⭐"
    if pct >= 75: return "⭐⭐⭐⭐"
    if pct >= 65: return "⭐⭐⭐"
    if pct >= 55: return "⭐⭐"
    return "⭐"

def exact_score_prediction(l_home, l_away):
    scores = []
    for h in range(5):
        for a in range(5):
            prob = poisson_probability(l_home, h) * poisson_probability(l_away, a)
            scores.append((f"{h}-{a}", prob * 100))
    scores.sort(key=lambda x: x[1], reverse=True)
    return ", ".join([f"{s[0]} ({int(s[1])}%)" for s in scores[:3]])

def kelly_stake(bankroll, probability, odds):
    p = probability / 100
    b = odds - 1
    q = 1 - p
    if b <= 0: return 0.0
    kelly = ((b * p) - q) / b
    # 10% Fractional Kelly για απόλυτη ασφάλεια κάβας
    return round(bankroll * max(0, kelly) * 0.1, 2)

# --- ΣΤΑΤΙΣΤΙΚΑ FOOTBALL-DATA.ORG ---
def get_advanced_stats(league_code):
    stats = {}
    standings_url = f"https://api.football-data.org/v4/competitions/{league_code}/standings"
    matches_url = f"https://api.football-data.org/v4/competitions/{league_code}/matches?status=FINISHED"

    try:
        st_res = requests.get(standings_url, headers=HEADERS_FOOTBALL, timeout=15)
        if st_res.status_code == 200:
            data = st_res.json()
            for standing in data.get('standings', []):
                if standing.get('type') == 'TOTAL':
                    for team in standing.get('table', []):
                        name = team['team']['name']
                        stats[name] = {
                            'overall_avg_scored': team['goalsFor'] / team['playedGames'] if team['playedGames'] > 0 else 1.0,
                            'overall_avg_conceded': team['goalsAgainst'] / team['playedGames'] if team['playedGames'] > 0 else 1.0,
                            'recent_goals_scored': [], 'recent_goals_conceded': []
                        }
        time.sleep(7)
        m_res = requests.get(matches_url, headers=HEADERS_FOOTBALL, timeout=15)
        if m_res.status_code == 200:
            all_matches = m_res.json().get('matches', [])
            for match in reversed(all_matches[-100:]):
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

def calculate_prediction(home, away, league_stats, real_odds_dict):
    if home not in league_stats or away not in league_stats:
        return "2-3 Goals", 55, "GG (58%)", "⭐", "1-1 (10%)", 1.90, 0.0

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
    stars = confidence_stars(pct)
    top_scores = exact_score_prediction(l_h, l_a)

    # Σύνδεση με πραγματικές αποδόσεις
    chosen_odds = 1.90
    match_key = f"{home}-{away}"
    if match_key in real_odds_dict:
        if tip == "Over 2.5" and "Over" in real_odds_dict[match_key]:
            chosen_odds = real_odds_dict[match_key]["Over"]
        elif tip == "Under 2.5" and "Under" in real_odds_dict[match_key]:
            chosen_odds = real_odds_dict[match_key]["Under"]

    stake = kelly_stake(BANKROLL, pct, chosen_odds)
    return tip, pct, cover, stars, top_scores, chosen_odds, stake

# --- MAIN EXECUTION ---
def main():
    init_database()
    predictions = []
    
    # Ώρα Ελλάδας (UTC+3)
    now_gr = datetime.utcnow() + timedelta(hours=3)
    today = now_gr.date()
    tomorrow = today + timedelta(days=1)
    day_after = today + timedelta(days=2)
    
    # Φίλτρο 48ώρου για να εμφανίζονται πάντα αγώνες
    allowed_dates = [today.strftime("%Y-%m-%d"), tomorrow.strftime("%Y-%m-%d"), day_after.strftime("%Y-%m-%d")]
    
    conn = sqlite3.connect("betting_history.db")
    cursor = conn.cursor()

    for code, info in LEAGUES.items():
        print(f"Ανάλυση & Λήψη αποδόσεων για: {info['name']}...")
        l_stats = get_advanced_stats(code)
        real_odds = get_real_odds(info['odds_market'])
        time.sleep(7)

        url = f"https://api.football-data.org/v4/competitions/{code}/matches"
        try:
            res = requests.get(url, headers=HEADERS_FOOTBALL, timeout=15)
            if res.status_code == 200:
                for m in res.json().get('matches', []):
                    if m['status'] in ['SCHEDULED', 'TIMED']:
                        gr_dt = datetime.strptime(m['utcDate'], "%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=3)
                        match_date_str = gr_dt.strftime("%Y-%m-%d")
                        
                        if match_date_str in allowed_dates:
                            home, away = m['homeTeam']['name'], m['awayTeam']['name']
                            
                            tip, pct, cover, stars, top_scores, odds, stake = calculate_prediction(home, away, l_stats, real_odds)
                            m_time = gr_dt.strftime("%H:%M")
                            
                            # Προσθήκη ημερομηνίας/ώρας στο format του αρχείου
                            m_date_display = gr_dt.strftime("%d/%m")
                            predictions.append(f"{info['name']}|{home} - {away}|{m_date_display} {m_time}|{tip} ({pct}%)|{stars}|Απόδοση: {odds}|Ποντάρισμα: {stake}€|Σκορ: {top_scores}")
                            
                            cursor.execute('''
                                INSERT INTO predictions (date, league, home_team, away_team, prediction, confidence, exact_scores, odds, stake)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                            ''', (match_date_str, info['name'], home, away, tip, stars, top_scores, odds, stake))
        except Exception as e:
            print(f"Σφάλμα στη λίγκα {info['name']}: {e}")
        time.sleep(7)

    conn.commit()
    conn.close()

    # Εγγραφή στο αρχείο TXT
    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        f.write(f"--- ΥΒΡΙΔΙΚΑ ΠΡΟΓΝΩΣΤΙΚΑ V3 ({now_gr.strftime('%d/%m/%Y %H:%M')}) ---\n")
        f.write("ΛΙΓΚΑ|ΑΓΩΝΑΣ|ΗΜΕΡ/ΩΡΑ|ΠΡΟΒΛΕΨΗ|ΕΜΠΙΣΤΟΣΥΝΗ|ΑΠΟΔΟΣΗ|KELLY STAKE|ΠΙΘΑΝΑ ΣΚΟΡ\n")
        for p in predictions: 
            f.write(p + "\n")
            
    print("✅ Το V3 Script ολοκληρώθηκε επιτυχώς! Το 'daily_predictions.txt' ενημερώθηκε.")

if __name__ == "__main__":
    main()

