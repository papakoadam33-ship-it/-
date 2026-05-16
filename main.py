import requests
import math
import time
from datetime import datetime, timedelta

# --- ΡΥΘΜΙΣΕΙΣ ---
# Το κλειδί σου από το RapidAPI
RAPID_API_KEY = "47d5da2fb8mshde110deccc94426p115d5ajsnd9cc939fa561"
HOST = "api-football-v1.p.rapidapi.com"

# Τα σωστά ID πρωταθλημάτων για το API-Football (Μαζί με Ελλάδα και Ligue 2!)
LEAGUES = {
    "197": "GREECE SUPER LEAGUE",
    "62": "LIGUE 2 (FRANCE)",
    "39": "PREMIER LEAGUE",
    "140": "LA LIGA",
    "135": "SERIE A",
    "78": "BUNDESLIGA",
    "61": "LIGUE 1"
}

def poisson_probability(lmbda, k):
    """Υπολογισμός πιθανότητας με κατανομή Poisson"""
    if lmbda <= 0: return 0
    return (math.exp(-lmbda) * (lmbda**k)) / math.factorial(k)

def get_advanced_stats(league_id):
    """Φέρνει στατιστικά για τις ομάδες από το API-Football v3"""
    stats = {}
    url = f"https://{HOST}/v3/standings"
    querystring = {"league": league_id, "season": "2025"}
    headers = {"x-rapidapi-key": RAPID_API_KEY, "x-rapidapi-host": HOST}
    
    try:
        res = requests.get(url, headers=headers, params=querystring, timeout=15).json()
        standings = res['response'][0]['league']['standings'][0]
        
        for row in standings:
            team_name = row['team']['name']
            played = row['all']['played']
            if played > 0:
                stats[team_name] = {
                    'overall_avg_scored': row['all']['goals']['for'] / played,
                    'overall_avg_conceded': row['all']['goals']['against'] / played
                }
        return stats
    except:
        return {}

def calculate_prediction(home, away, league_stats):
    """Υπολογίζει Over 2.5 και GG με την κατανομή Poisson"""
    if home not in league_stats or away not in league_stats:
        return "2-3 Goals (55%)", "GG (58%)"

    h_s = league_stats[home]
    a_s = league_stats[away]

    # Υπολογισμός αναμενόμενων γκολ (Lambda)
    l_h = h_s['overall_avg_scored'] * (a_s['overall_avg_conceded'] / 1.2)
    l_a = a_s['overall_avg_scored'] * (h_s['overall_avg_conceded'] / 1.2)
    l_total = l_h + l_a

    # Πιθανότητα Over 2.5
    prob_under_2_5 = sum(poisson_probability(l_total, k) for k in range(3))
    prob_over = (1 - prob_under_2_5) * 100
    
    # Πιθανότητα GG
    prob_gg = (1 - poisson_probability(l_h, 0)) * (1 - poisson_probability(l_a, 0)) * 100

    if prob_over > 60: tip = f"Over 2.5 ({int(prob_over)}%)"
    elif prob_over < 40: tip = f"Under 2.5 ({int(100-prob_over)}%)"
    else: tip = f"2-3 Goals (55%)"

    cover = f"GG ({int(prob_gg)}%)" if prob_gg > 50 else f"No GG ({int(100-prob_gg)}%)"
    
    return tip, cover

def main():
    predictions = []
    now_gr = datetime.utcnow() + timedelta(hours=3)
    today = now_gr.strftime("%Y-%m-%d")
    tomorrow = (now_gr + timedelta(days=1)).strftime("%Y-%m-%d")
    
    for league_id, label in LEAGUES.items():
        l_stats = get_advanced_stats(league_id)
        time.sleep(1.5) # Καθυστέρηση για να μην μας μπλοκάρει το API
        
        url = f"https://{HOST}/v3/fixtures"
        querystring = {"league": league_id, "season": "2025", "from": today, "to": tomorrow}
        headers = {"x-rapidapi-key": RAPID_API_KEY, "x-rapidapi-host": HOST}
        
        try:
            res = requests.get(url, headers=headers, params=querystring).json()
            for m in res.get('response', []):
                home = m['teams']['home']['name']
                away = m['teams']['away']['name']
                
                # Μετατροπή ώρας σε Ελλάδας
                utc_dt = datetime.fromisoformat(m['fixture']['date'].replace('Z', '+00:00'))
                gr_dt = utc_dt + timedelta(hours=3)
                
                tip, cover = calculate_prediction(home, away, l_stats)
                display_time = gr_dt.strftime("%d/%m %H:%M")
                
                predictions.append(f"{label}|{home} - {away}|{display_time}|{tip}|{cover}")
        except:
            continue
        time.sleep(1.5)

    # Εγγραφή στο αρχείο daily_predictions.txt
    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        timestamp = now_gr.strftime("%d/%m/%Y %H:%M")
        f.write(f"--- ΠΡΟΓΝΩΣΤΙΚΑ {timestamp} ---\n")
        f.write("ΛΙΓΚΑ|ΑΓΩΝΑΣ|ΩΡΑ|ΠΡΟΒΛΕΨΗ|ΚΑΛΥΨΗ\n")
        
        if not predictions:
            f.write("INFO|Δεν υπάρχουν αγώνες για σήμερα/αύριο.|-| - | - \n")
        else:
            for p in predictions:
                f.write(p + "\n")

if __name__ == "__main__":
    main()

