import requests
import math
import time
from datetime import datetime, timezone, timedelta
import hashlib

# --- ΡΥΘΜΙΣΕΙΣ ---
API_KEY = "a963742bcd5642afbe8c842d057f25ad"
HEADERS = { "X-Auth-Token": API_KEY }

# Οι 8 λίγκες στις οποίες έχουμε πρόσβαση για πλήρη στατιστικά Poisson
POISSON_LEAGUES = {
    "PL": "PREMIER LEAGUE",
    "PD": "LA LIGA",
    "SA": "SERIE A",
    "BL1": "BUNDESLIGA",
    "FL1": "LIGUE 1",
    "DED": "EREDIVISIE",
    "PPL": "PRIMEIRA LIGA",
    "ELC": "CHAMPIONSHIP"
}

# Όλο το mapping των λιγκών για το UI σου
LEAGUES_INFO = {
    "Premier League": "🏴󠁧󠁢󠁥󠁮󠁧󠁿 ΠΡΕΜΙΕΡ ΛΙΓΚ",
    "Championship": "🏴󠁧󠁢󠁥󠁮󠁧󠁿 ΤΣΑΜΠΙΟΝΣΙΠ",
    "UEFA Champions League": "🇪🇺 ΤΣΑΜΠΙΟΝΣ ΛΙΓΚ",
    "Primera Division": "🇪🇸 ΛΑ ΛΙΓΚΑ",
    "Serie A": "🇮🇹 ΣΕΡΙΕ Α",
    "Bundesliga": "🇩🇪 ΜΠΟΥΝΤΕΣΛΙΓΚΑ",
    "Ligue 1": "🇫🇷 ΛΙΓΚ 1",
    "Eredivisie": "🇳🇱 ΟΛΛΑΝΔΙΑ",
    "Primeira Liga": "🇵🇹 ΠΟΡΤΟΓΑΛΙΑ",
    "Campeonato Brasileiro Série A": "🇧🇷 BRAZIL SERIE A",
    "Copa Libertadores": "🏆 COPA LIBERTADORES"
}

def poisson_probability(lmbda, k):
    if lmbda <= 0: return 0
    return (math.exp(-lmbda) * (lmbda**k)) / math.factorial(k)

def get_advanced_stats(league_code):
    stats = {}
    standings_url = f"https://api.football-data.org/v4/competitions/{league_code}/standings"
    matches_url = f"https://api.football-data.org/v4/competitions/{league_code}/matches?status=FINISHED"

    try:
        st_res = requests.get(standings_url, headers=HEADERS, timeout=12)
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

        m_res = requests.get(matches_url, headers=HEADERS, timeout=12)
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
    except:
        return {}

def calculate_poisson_prediction(home, away, league_stats):
    if home not in league_stats or away not in league_stats:
        return None
        
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

    prob_1, prob_x, prob_2 = 0, 0, 0
    prob_over_1_5 = 0
    
    for h_goals in range(6):
        for a_goals in range(6):
            p_score = poisson_probability(l_h, h_goals) * poisson_probability(l_a, a_goals)
            if h_goals > a_goals: prob_1 += p_score
            elif h_goals == a_goals: prob_x += p_score
            else: prob_2 += p_score
            if (h_goals + a_goals) > 1: prob_over_1_5 += p_score

    p_1, p_x, p_2, p_o15 = prob_1*100, prob_x*100, prob_2*100, prob_over_1_5*100
    prob_over_2_5 = (1 - sum(poisson_probability(l_total, k) for k in range(3))) * 100
    prob_gg = (1 - poisson_probability(l_h, 0)) * (1 - poisson_probability(l_a, 0)) * 100

    return format_final_tip(p_1, p_x, p_2, p_o15, prob_over_2_5, prob_gg)

def calculate_simulated_prediction(home_team, away_team, league_name):
    """
    Έξυπνη Ψευδο-Προσομοίωση για κλειδωμένες λίγκες. 
    Χρησιμοποιεί ένα σταθερό Hash (Deterministic) βασισμένο στα ονόματα των ομάδων,
    ώστε το προγνωστικό να ΜΗΝ αλλάζει σε κάθε refresh της εφαρμογής (να μένει σταθερό όλη μέρα).
    """
    combined_string = f"{home_team}-{away_team}-{league_name}"
    hash_value = int(hashlib.md5(combined_string.encode('utf-8')).hexdigest(), 16)
    
    # Καθορισμός στυλ λίγκας (π.χ. Λατινική Αμερική = πιο κλειστά ματς / Under)
    is_under_league = any(x in league_name for x in ["Brasileiro", "Libertadores"])
    
    # Παραγωγή σταθερών "ψευδο-στατιστικών" βάσει του Hash
    stat_score = hash_value % 100
    goal_score = (hash_value // 100) % 100
    
    # 1X2 Πιθανότητες
    if stat_score < 42:
        p_1, p_x, p_2 = 52.0, 28.0, 20.0  # Προβάδισμα έδρας
    elif stat_score < 75:
        p_1, p_x, p_2 = 33.0, 35.0, 32.0  # Ντέρμπι / Ισορροπία
    else:
        p_1, p_x, p_2 = 22.0, 26.0, 52.0  # Διπλό
        
    # Γκολ Πιθανότητες
    if is_under_league:
        p_o15 = 58.0 + (goal_score % 15)
        prob_over_2_5 = 35.0 + (goal_score % 15)
        prob_gg = 42.0 + (goal_score % 15)
    else:
        p_o15 = 72.0 + (goal_score % 15)
        prob_over_2_5 = 54.0 + (goal_score % 15)
        prob_gg = 55.0 + (goal_score % 15)

    return format_final_tip(p_1, p_x, p_2, p_o15, prob_over_2_5, prob_gg)

def format_final_tip(p_1, p_x, p_2, p_o15, prob_over_2_5, prob_gg):
    if p_1 > 46 and p_o15 > 68:
        tip, pct = "1 & Over 1.5", int((p_1 + p_o15) / 2)
    elif p_2 > 46 and p_o15 > 68:
        tip, pct = "2 & Over 1.5", int((p_2 + p_o15) / 2)
    elif (p_1 + p_x) > 68 and p_o15 > 68:
        tip, pct = "1X & Over 1.5", int(((p_1 + p_x) + p_o15) / 2)
    elif (p_2 + p_x) > 68 and p_o15 > 68:
        tip, pct = "X2 & Over 1.5", int(((p_2 + p_x) + p_o15) / 2)
    elif prob_over_2_5 > 55:
        tip, pct = "Over 2.5", int(prob_over_2_5)
    else:
        tip, pct = "Under 2.5", int(100 - prob_over_2_5)

    cover = f"Goal-Goal ({int(prob_gg)}%)" if prob_gg > 50 else f"No GG ({int(100-prob_gg)}%)"
    return tip, pct, cover

def main():
    predictions = []
    # Ώρα Ελλάδας (UTC+3)
    now_gr = datetime.now(timezone.utc) + timedelta(hours=3)
    today_str = now_gr.strftime("%Y-%m-%d")
    
    print(f"Starting HYBRID Pro-Bet Engine for: {today_str}")
    
    # 1. Προ-φόρτωση στατιστικών Poisson για τις δωρεάν λίγκες
    poisson_data = {}
    for code, label in POISSON_LEAGUES.items():
        print(f"Pre-loading Poisson data for {label}...")
        stats = get_advanced_stats(code)
        if stats:
            poisson_data[code] = stats
        time.sleep(6) # Σεβασμός στο rate limit

    # 2. Κλήση του κεντρικού URL για ΟΛΟΥΣ τους αγώνες της ημέρας
    url = "https://api.football-data.org/v4/matches"
    try:
        res = requests.get(url, headers=HEADERS, timeout=20).json()
        if "matches" in res:
            for m in res["matches"]:
                league_name = m['competition']['name']
                league_code = m['competition']['code']
                
                # Φιλτράρισμα: Κρατάμε μόνο τις λίγκες που έχουμε στο LEAGUES_INFO
                if league_name not in LEAGUES_INFO: 
                    continue
                
                # Φιλτράρισμα κατάστασης: Εμφάνιση SCHEDULED, LIVE και IN_PLAY αγώνων
                if m['status'] in ['SCHEDULED', 'TIMED', 'LIVE', 'IN_PLAY']:
                    utc_dt = datetime.strptime(m['utcDate'], "%Y-%m-%dT%H:%M:%SZ")
                    gr_dt = utc_dt.replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=3)))
                    match_date_str = gr_dt.strftime("%Y-%m-%d")
                    
                    # Έλεγχος αν ο αγώνας διεξάγεται σήμερα
                    if match_date_str == today_str:
                        home = m['homeTeam']['name']
                        away = m['awayTeam']['name']
                        match_time = gr_dt.strftime("%H:%M")
                        league_label = LEAGUES_INFO[league_name].upper()
                        
                        # Απόφαση Μηχανής: Αληθινή Poisson ή Έξυπνη Προσομοίωση;
                        if league_code in poisson_data:
                            # Καθαρά Μαθηματικά
                            result = calculate_poisson_prediction(home, away, poisson_data[league_code])
                            if result:
                                tip, pct, cover = result
                            else:
                                tip, pct, cover = calculate_simulated_prediction(home, away, league_name)
                        else:
                            # Έξυπνη Προσομοίωση (για Βραζιλία, Champions League κλπ)
                            tip, pct, cover = calculate_simulated_prediction(home, away, league_name)
                        
                        main_display = f"{tip} ({pct}%)"
                        predictions.append(f"{league_label}|{home} - {away}|{match_time}|{main_display}|{cover}")
                        
    except Exception as e:
        print(f"General Error: {e}")

    # 3. Εγγραφή στο txt αρχείο έτοιμο για το App σου
    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        timestamp_date = now_gr.strftime("%d/%m/%Y")
        timestamp_time = now_gr.strftime("%H:%M")
        f.write(f"ΗΜΕΡΟΜΗΝΙΑ|{timestamp_date}|{timestamp_time}\n")
        
        if not predictions:
            f.write("INFO|Δεν υπάρχουν σημερινοί αγώνες.|-| - (0%) | - \n")
        else:
            for p in predictions:
                f.write(p + "\n")
            print(f"Successfully generated {len(predictions)} hybrid predictions!")

if __name__ == "__main__":
    main()
