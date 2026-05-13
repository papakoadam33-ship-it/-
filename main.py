import requests
import math
import time
from datetime import datetime

API_KEY = "a963742bcd5642afbe8c842d057f25ad"
HEADERS = { "X-Auth-Token": API_KEY }

def get_h2h_factor(home_team, away_team, league_code):
    """Ψάχνει προηγούμενα ματς των δύο ομάδων στη τρέχουσα σεζόν"""
    url = f"https://api.football-data.org/v4/competitions/{league_code}/matches?status=FINISHED"
    h2h_goals = []
    try:
        res = requests.get(url, headers=HEADERS).json()
        for m in res.get('matches', []):
            # Ελέγχουμε αν οι ομάδες έχουν παίξει μεταξύ τους (ανεξαρτήτως έδρας)
            teams = [m['homeTeam']['name'], m['awayTeam']['name']]
            if home_team in teams and away_team in teams:
                total_goals = m['score']['fullTime']['home'] + m['score']['fullTime']['away']
                h2h_goals.append(total_goals)
        
        if not h2h_goals: return 1.0 # Ουδέτερος παράγοντας αν δεν έχουν παίξει
        return sum(h2h_goals) / len(h2h_goals)
    except:
        return 1.0

def calculate_final_prediction(home, away, league_stats, league_code):
    # 1. Υπολογισμός Lambda βάσει φόρμας (όπως πριν)
    l_h, l_a = calculate_lambda(home, away, league_stats) # Από τον προηγούμενο κώδικα
    base_expected_goals = l_h + l_a
    
    # 2. Ενσωμάτωση H2H
    h2h_avg = get_h2h_factor(home, away, league_code)
    
    # Τελικό Adjusted Lambda (Μίξη φόρμας και παράδοσης)
    final_lambda = (base_expected_goals * 0.8) + (h2h_avg * 0.2)
    
    # 3. Πιθανότητες Poisson
    p0 = (math.exp(-final_lambda) * (final_lambda**0)) / 1 
    p1 = (math.exp(-final_lambda) * (final_lambda**1)) / 1
    p2 = (math.exp(-final_lambda) * (final_lambda**2)) / 2
    
    prob_over_2_5 = (1 - (p0 + p1 + p2)) * 100
    
    # Λογική Επιλογής Σημείου
    if prob_over_2_5 > 65:
        return f"🔥 Over 2.5 ({int(prob_over_2_5)}%)"
    elif prob_over_2_5 < 35:
        return f"❄️ Under 2.5 ({int(100 - prob_over_2_5)}%)"
    else:
        return "⚖️ 2-3 Goals (Medium Risk)"

# Κύρια ροή
def run_expert_system():
    # Περιορίζουμε σε 1 λίγκα για να μη φάμε rate limit λόγω του έξτρα H2H call
    leagues = {"PL": "Premier League"} 
    
    for code, name in leagues.items():
        stats = get_advanced_stats(code)
        time.sleep(2)
        
        url = f"https://api.football-data.org/v4/competitions/{code}/matches?status=SCHEDULED"
        matches = requests.get(url, headers=HEADERS).json().get('matches', [])[:5]
        
        print(f"\n--- ΠΡΟΓΝΩΣΤΙΚΑ ΓΙΑ {name.upper()} ---")
        for m in matches:
            h = m['homeTeam']['name']
            a = m['awayTeam']['name']
            
            prediction = calculate_final_prediction(h, a, stats, code)
            print(f"🏟️ {h} vs {a}")
            print(f"💡 Tip: {prediction}\n")
            time.sleep(2) # Πολύ σημαντικό λόγω των πολλών requests

if __name__ == "__main__":
    run_expert_system()
