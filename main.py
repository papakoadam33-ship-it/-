import requests
import math
import time
from datetime import datetime

# --- ΡΥΘΜΙΣΕΙΣ ΚΑΙ ΜΕΤΑΦΡΑΣΕΙΣ ---
API_KEY = "a963742bcd5642afbe8c842d057f25ad"
HEADERS = { "X-Auth-Token": API_KEY }

# Λίστα με τα Codes των πρωταθλημάτων που υποστηρίζει το free tier
LEAGUES = {
    "PL": "🏴󠁧󠁢󠁥󠁮󠁧󠁿 PREMIER LEAGUE",
    "PD": "🇪🇸 LA LIGA",
    "SA": "🇮🇹 SERIE A",
    "BL1": "🇩🇪 BUNDESLIGA",
    "FL1": "🇫🇷 LIGUE 1"
}

def poisson_probability(lmbda, k):
    """Υπολογίζει την πιθανότητα Poisson για k γκολ"""
    if lmbda <= 0: return 0
    return (math.exp(-lmbda) * (lmbda**k)) / math.factorial(k)

def get_advanced_stats(league_code):
    """Τραβάει στατιστικά σεζόν και φόρμα τελευταίων 5 αγώνων"""
    stats = {}
    standings_url = f"https://api.football-data.org/v4/competitions/{league_code}/standings"
    matches_url = f"https://api.football-data.org/v4/competitions/{league_code}/matches?status=FINISHED"

    try:
        # 1. Γενική Βαθμολογία
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

        # 2. Φόρμα (Τελευταία 100 ματς της λίγκας για να βρούμε τα 5 κάθε ομάδας)
        m_res = requests.get(matches_url, headers=HEADERS, timeout=15)
        if m_res.status_code == 200:
            for match in reversed(m_res.json()['matches'][-100:]):
                h_team, a_team = match['homeTeam']['name'], match['awayTeam']['name']
                h_score, a_score = match['score']['fullTime']['home'], match['score']['fullTime']['away']

                if h_team in stats and len(stats[h_team]['recent_goals_scored']) < 5:
                    stats[h_team]['recent_goals_scored'].append(h_score)
                    stats[h_team]['recent_goals_conceded'].append(a_score)
                if a_team in stats and len(stats[a_team]['recent_goals_scored']) < 5:
                    stats[a_team]['recent_goals_scored'].append(a_score)
                    stats[a_team]['recent_goals_conceded'].append(h_score)
        return stats
    except Exception as e:
        print(f"Error fetching stats: {e}")
        return {}

def calculate_prediction(home, away, league_stats):
    """Κύριος αλγόριθμος πρόβλεψης"""
    if home not in league_stats or away not in league_stats:
        return "N/A", "N/A"

    h_s, a_s = league_stats[home], league_stats[away]
    
    # Weighted Average (70% Φόρμα - 30% Σεζόν)
    def get_val(recent, overall):
        r_avg = sum(recent)/len(recent) if recent else overall
        return (r_avg * 0.7) + (overall * 0.3)

    l_h = get_val(h_s['recent_goals_scored'], h_s['overall_avg_scored']) * (get_val(a_s['recent_goals_conceded'], a_s['overall_avg_conceded']) / 1.3)
    l_a = get_val(a_s['recent_goals_scored'], a_s['overall_avg_scored']) * (get_val(h_s['recent_goals_conceded'], h_s['overall_avg_conceded']) / 1.3)
    l_total = l_h + l_a

    # Πιθανότητες
    p_under_2_5 = sum(poisson_probability(l_total, k) for k in range(3))
    prob_over = (1 - p_under_2_5) * 100
    prob_gg = (1 - poisson_probability(l_h, 0)) * (1 - poisson_probability(l_a, 0)) * 100

    # Επιλογή σημείου
    if prob_over > 60: tip = f"Over 2.5 ({int(prob_over)}%)"
    elif prob_over < 40: tip = f"Under 2.5 ({int(100-prob_over)}%)"
    else: tip = "2-3 Goals"

    cover = "GG" if prob_gg > 52 else "No GG"
    return tip, cover

def main():
    predictions = []
    print("🚀 Έναρξη ανάλυσης...")

    for code, label in LEAGUES.items():
        print(f"📊 Επεξεργασία: {label}")
        l_stats = get_advanced_stats(code)
        time.sleep(2) # Rate limit protection

        url = f"https://api.football-data.org/v4/competitions/{code}/matches?status=SCHEDULED"
        try:
            res = requests.get(url, headers=HEADERS).json()
            for m in res.get('matches', [])[:8]: # 8 ματς ανά λίγκα
                home, away = m['homeTeam']['name'], m['awayTeam']['name']
                tip, cover = calculate_prediction(home, away, l_stats)
                
                dt = datetime.strptime(m['utcDate'], "%Y-%m-%dT%H:%M:%SZ")
                m_time = f"{(dt.hour + 3) % 24:02d}:{dt.minute:02d}"
                
                predictions.append(f"{label}|{home} - {away}|{m_time}|{tip}|{cover}")
        except: continue
        time.sleep(2)

    # Αποθήκευση σε αρχείο
    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        now = datetime.now().strftime("%d/%m/%Y %H:%M")
        f.write(f"--- ΠΡΟΓΝΩΣΤΙΚΑ {now} ---\n")
        f.write("ΛΙΓΚΑ|ΑΓΩΝΑΣ|ΩΡΑ|ΠΡΟΒΛΕΨΗ|ΚΑΛΥΨΗ\n")
        for p in predictions: f.write(p + "\n")
    print("✅ Το αρχείο daily_predictions.txt ενημερώθηκε!")

if __name__ == "__main__":
    main()
