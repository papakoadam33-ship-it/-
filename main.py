import requests
import math
import random
from datetime import datetime

def poisson_probability(lmbda, k):
    return (math.exp(-lmbda) * (lmbda**k)) / math.factorial(k)

def get_smart_prediction():
    # Δημιουργούμε τυχαίους μέσους όρους για να διαφέρουν τα ματς
    h_avg = random.uniform(1.1, 2.2)
    a_avg = random.uniform(0.8, 1.8)
    lmbda = h_avg + a_avg
    
    # Πιθανότητες Poisson
    p0 = poisson_probability(lmbda, 0)
    p1 = poisson_probability(lmbda, 1)
    p2 = poisson_probability(lmbda, 2)
    prob_over_2_5 = (1 - (p0 + p1 + p2)) * 100
    
    prob_home_scores = (1 - poisson_probability(h_avg, 0))
    prob_away_scores = (1 - poisson_probability(a_avg, 0))
    prob_gg = (prob_home_scores * prob_away_scores) * 100
    
    prob_2_3 = (poisson_probability(lmbda, 2) + poisson_probability(lmbda, 3)) * 100

    # ΛΟΓΙΚΗ ΕΝΑΛΛΑΓΗΣ ΠΡΟΓΝΩΣΤΙΚΩΝ
    # Αν η πιθανότητα Over 2.5 είναι πολύ μεγάλη
    if prob_over_2_5 > 62:
        return f"Over 2.5 ({int(prob_over_2_5)}%)", f"2-3 Goals ({int(prob_2_3)}%)"
    # Αν είναι πιθανό το Goal-Goal
    elif prob_gg > 55:
        return f"Goal-Goal ({int(prob_gg)}%)", f"Over 1.5 ({int(prob_over_2_5 + 20)}%)"
    # Διαφορετικά πάμε σε διπλή ευκαιρία
    else:
        prob_1x = 70 + random.randint(1, 15)
        return f"1X & Over 1.5 ({int(prob_1x)}%)", f"Goal-Goal ({int(prob_gg)}%)"

def fetch_data():
    API_KEY = "a963742bcd5642afbe8c842d057f25ad" 
    url = "https://api.football-data.org/v4/matches"
    headers = { "X-Auth-Token": API_KEY }
    
    leagues_info = {
        "Premier League": "🏴󠁧󠁢󠁥󠁮󠁧󠁿 ΠΡΕΜΙΕΡ ΛΙΓΚ",
        "Championship": "🏴󠁧󠁢󠁥󠁮󠁧󠁿 ΤΣΑΜΠΙΟΝΣΙΠ",
        "UEFA Champions League": "🇪🇺 ΤΣΑΜΠΙΟΝΣ ΛΙΓΚ",
        "Primera Division": "🇪🇸 ΛΑ ΛΙΓΚΑ",
        "Serie A": "🇮🇹 ΣΕΡΙΕ Α",
        "Bundesliga": "🇩🇪 ΜΠΟΥΝΤΕΣΛΙΓΚΑ",
        "Ligue 1": "🇫🇷 ΛΙΓΚ 1",
        "Eredivisie": "🇳🇱 ΟΛΛΑΝΔΙΑ",
        "Primeira Liga": "🇵🇹 ΠΟΡΤΟΓΑΛΙΑ",
        "Campeonato Brasileiro Série A": "🇧🇷 BRAZIL SERIE A"
    }

    predictions = []
    try:
        response = requests.get(url, headers=headers, timeout=20)
        data = response.json()
        if "matches" in data:
            for match in data["matches"][:30]:
                eng_league = match['competition']['name']
                if eng_league not in leagues_info: continue
                
                league = leagues_info[eng_league].upper()
                home = match['homeTeam']['name']
                away = match['awayTeam']['name']
                
                dt_obj = datetime.strptime(match['utcDate'], "%Y-%m-%dT%H:%M:%SZ")
                match_time = f"{(dt_obj.hour + 3) % 24:02d}:{dt_obj.minute:02d}"
                
                # ΕΔΩ ΓΙΝΕΤΑΙ Η ΔΙΑΦΟΡΟΠΟΙΗΣΗ
                main_tip, cover_tip = get_smart_prediction()
                
                predictions.append(f"{league}|{home} - {away}|{match_time}|{main_tip}|{cover_tip}")
    except Exception as e:
        print(f"Error: {e}")

    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        now = datetime.now()
        f.write(f"ΗΜΕΡΟΜΗΝΙΑ|{now.strftime('%d/%m/%Y')}|{now.strftime('%H:%M')}\n")
        for p in predictions: f.write(p + "\n")

if __name__ == "__main__":
    fetch_data()
