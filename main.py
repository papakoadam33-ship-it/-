import requests
import math
import time
from datetime import datetime, timedelta

# --- ΡΥΘΜΙΣΕΙΣ ---
API_KEY = "a963742bcd5642afbe8c842d057f25ad"
HEADERS = { "X-Auth-Token": API_KEY }

# Λίστα με τα Codes των πρωταθλημάτων που υποστηρίζει το free tier
LEAGUES = {
    "PL": "PREMIER LEAGUE",
    "PD": "LA LIGA",
    "SA": "SERIE A",
    "BL1": "BUNDESLIGA",
    "FL1": "LIGUE 1"
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

        # 2. Φόρμα (Τελευταία 120 ματς της λίγκας για να βρούμε τα 5 κάθε ομάδας)
        m_res = requests.get(matches_url, headers=HEADERS, timeout=15)
        if m_res.status_code == 200:
            for match in reversed(m_res.json()['matches'][-120:]):
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
        print(f"Error fetching stats: {e}")
        return {}

def calculate_prediction(home, away, league_stats):
    """Κύριος αλγόριθμος πρόβλεψης"""
    if home not in league_stats or away not in league_stats:
        return "N/A (0%)", "N/A (0%)"

    h_s, a_s = league_stats[home], league_stats[away]
    
    # Weighted Average (70% Φόρμα - 30% Σεζόν)
    def get_val(recent, overall):
        r_avg = sum(recent)/len(recent) if recent else overall
        return (r_avg * 0.7) + (overall * 0.3)

    # Αναμενόμενα γκολ (λ)
    l_h = get_val(h_s['recent_goals_scored'], h_s['overall_avg_scored']) * (get_val(a_s['recent_goals_conceded'], a_s['overall_avg_conceded']) / 1.3)
    l_a = get_val(a_s['recent_goals_scored'], a_s['overall_avg_scored']) * (get_val(h_s['recent_goals_conceded'], h_s['overall_avg_conceded']) / 1.3)
    l_total = l_h + l_a

    # Πιθανότητα Under/Over 2.5
    prob_under_2_5 = sum(poisson_probability(l_total, k) for k in range(3))
    prob_over = (1 - prob_under_2_5) * 100
    
    # Πιθανότητα Goal/Goal
    prob_gg = (1 - poisson_probability(l_h, 0)) * (1 - poisson_probability(l_a, 0)) * 100

    # Επιλογή Κύριου Tip
    if prob_over > 60: tip = f"Over 2.5 ({int(prob_over)}%)"
    elif prob_over < 40: tip = f"Under 2.5 ({int(100-prob_over)}%)"
    else: tip = f"2-3 Goals (55%)"

    # Επιλογή Κάλυψης (Με Ποσοστό)
    c_label = "GG" if prob_gg > 50 else "No GG"
    c_pct = int(prob_gg) if prob_gg > 50 else int(100 - prob_gg)
    cover = f"{c_label} ({c_pct}%)"
    
    return tip, cover

def main():
    predictions = []
    # Χρήση ώρας Ελλάδας (UTC+3) για το φιλτράρισμα
    now_gr = datetime.utcnow() + timedelta(hours=3)
    today_str = now_gr.strftime("%Y-%m-%d")
    
    for code, label in LEAGUES.items():
        print(f"📊 Επεξεργασία: {label}...")
        l_stats = get_advanced_stats(code)
        time.sleep(2) # Σεβασμός στο rate limit του API

        url = f"https://api.football-data.org/v4/competitions/{code}/matches?status=SCHEDULED"
        try:
            res = requests.get(url, headers=HEADERS).json()
            for m in res.get('matches', []):
                # Φίλτρο: Μόνο αγώνες που διεξάγονται σήμερα
                match_date = m['utcDate'].split("T")[0]
                if match_date != today_str:
                    continue

                home, away = m['homeTeam']['name'], m['awayTeam']['name']
                tip, cover = calculate_prediction(home, away, l_stats)
                
                # Μετατροπή ώρας σε Ελλάδας (UTC+3)
                utc_dt = datetime.strptime(m['utcDate'], "%Y-%m-%dT%H:%M:%SZ")
                gr_dt = utc_dt + timedelta(hours=3)
                m_time = gr_dt.strftime("%H:%M")
                
                predictions.append(f"{label}|{home} - {away}|{m_time}|{tip}|{cover}")
        except Exception as e:
            print(f"Σφάλμα στη λίγκα {label}: {e}")
            continue
        time.sleep(2)

    # Αποθήκευση στο αρχείο για το Streamlit
    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        timestamp = now_gr.strftime("%d/%m/%Y %H:%M")
        f.write(f"--- ΠΡΟΓΝΩΣΤΙΚΑ {timestamp} ---\n")
        f.write("ΛΙΓΚΑ|ΑΓΩΝΑΣ|ΩΡΑ|ΠΡΟΒΛΕΨΗ|ΚΑΛΥΨΗ\n")
        if not predictions:
            f.write("INFO|Δεν υπάρχουν άλλοι αγώνες για σήμερα.|-| - | - \n")
        else:
            for p in predictions:
                f.write(p + "\n")
    print("✅ Το αρχείο daily_predictions.txt ενημερώθηκε!")

if __name__ == "__main__":
    main()
