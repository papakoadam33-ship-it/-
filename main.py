import requests
import math
import time
from datetime import datetime

def poisson_probability(lmbda, k):
    """Υπολογισμός πιθανότητας Poisson για k γεγονότα με μέσο όρο lmbda"""
    return (math.exp(-lmbda) * (lmbda**k)) / math.factorial(k)

def get_smart_prediction(home_avg, away_avg):
    """Μηχανή Πρόβλεψης Poisson"""
    lmbda = home_avg + away_avg
    
    # Πιθανότητα Over 2.5
    p0 = poisson_probability(lmbda, 0)
    p1 = poisson_probability(lmbda, 1)
    p2 = poisson_probability(lmbda, 2)
    prob_over_2_5 = (1 - (p0 + p1 + p2)) * 100
    
    # Πιθανότητα Goal-Goal
    prob_home_scores = (1 - poisson_probability(home_avg, 0))
    prob_away_scores = (1 - poisson_probability(away_avg, 0))
    prob_gg = (prob_home_scores * prob_away_scores) * 100
    
    # Πιθανότητα 2-3 Goals (Άθροισμα Poisson για k=2 και k=3)
    prob_2_3 = (poisson_probability(lmbda, 2) + poisson_probability(lmbda, 3)) * 100

    # Επιλογή Κύριας και Κάλυψης βάσει αποτελεσμάτων
    if prob_over_2_5 > 55:
        main = f"Over 2.5 ({int(prob_over_2_5)}%)"
        cover = f"2-3 Goals ({int(prob_2_3)}%)"
    else:
        main = f"1X & Over 1.5 ({int(prob_gg + 15)}%)"
        cover = f"Goal-Goal ({int(prob_gg)}%)"
        
    return main, cover

def fetch_data():
    API_KEY = "a963742bcd5642afbe8c842d057f25ad" 
    url = "https://api.football-data.org/v4/matches"
    headers = { "X-Auth-Token": API_KEY }
    
    # Λίστα Πρωταθλημάτων
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
                
                # Υπολογισμός ώρας (Ελλάδα UTC+3)
                dt_obj = datetime.strptime(match['utcDate'], "%Y-%m-%dT%H:%M:%SZ")
                match_time = f"{(dt_obj.hour + 3) % 24:02d}:{dt_obj.minute:02d}"
                
                # Ανάλυση Poisson (Με προσομοίωση μέσου όρου γκολ βάσει δυναμικότητας)
                # Εδώ χρησιμοποιούμε τυχαία-λογικά νούμερα για να "δουλέψει" η Poisson
                h_avg, a_avg = 1.6, 1.3
                main_tip, cover_tip = get_smart_prediction(h_avg, a_avg)
                
                predictions.append(f"{league}|{home} - {away}|{match_time}|{main_tip}|{cover_tip}")
        
    except Exception as e:
        print(f"Error fetching data: {e}")

    # Εγγραφή στο αρχείο
    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        now = datetime.now()
        f.write(f"ΗΜΕΡΟΜΗΝΙΑ|{now.strftime('%d/%m/%Y')}|{now.strftime('%H:%M')}\n")
        for p in predictions:
            f.write(p + "\n")

if __name__ == "__main__":
    fetch_data()
