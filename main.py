import requests
import math
from datetime import datetime, timedelta

# ΣΥΝΑΡΤΗΣΗ POISSON
def poisson_probability(lmbda, x):
    return (math.exp(-lmbda) * (lmbda**x)) / math.factorial(x)

def calculate_tips(h_avg, a_avg):
    # Η "προσδοκία γκολ" (mu) για το ματς
    mu = (h_avg + a_avg) / 2
    
    # Πιθανότητα για 0, 1, 2 γκολ
    p0 = poisson_probability(mu, 0)
    p1 = poisson_probability(mu, 1)
    p2 = poisson_probability(mu, 2)
    
    # Πιθανότητα για Over 2.5 (1 - πιθανότητα για 0,1,2 γκολ)
    prob_over = (1 - (p0 + p1 + p2)) * 100
    
    # Πιθανότητα για Goal-Goal (εκτίμηση βάσει mu)
    prob_gg = (1 - math.exp(-mu/1.2)) * 90 
    
    return round(prob_over), round(prob_gg), mu

def get_stats(headers):
    leagues = ['PL', 'PD', 'BL1', 'SA', 'FL1', 'ELC', 'DED', 'PPL', 'BSA']
    stats = {}
    for league in leagues:
        try:
            url = f"https://api.football-data.org/v4/competitions/{league}/standings"
            res = requests.get(url, headers=headers).json()
            if 'standings' in res:
                for row in res['standings'][0]['table']:
                    team = row['team']['name']
                    m = row['playedGames']
                    if m > 0:
                        avg = (row['goalsFor'] + row['goalsAgainst']) / m
                        stats[team] = avg
        except: continue
    return stats

def run():
    headers = { 'X-Auth-Token': 'a1a4edf072dc4b2c8153fced44c88de9' }
    team_stats = get_stats(headers)
    url = "https://api.football-data.org/v4/matches"
    
    try:
        data = requests.get(url, headers=headers).json()
        now_gr = datetime.utcnow() + timedelta(hours=3)
        output = f"ΗΜΕΡΟΜΗΝΙΑ|{now_gr.strftime('%d/%m/%Y')}|{now_gr.strftime('%H:%M')}\n"
        
        for m in data.get('matches', []):
            match_utc = datetime.strptime(m['utcDate'], '%Y-%m-%dT%H:%M:%SZ')
            match_gr = match_utc + timedelta(hours=3)
            
            if match_gr > now_gr:
                h_team, a_team = m['homeTeam']['name'], m['awayTeam']['name']
                h_avg = team_stats.get(h_team, 2.5)
                a_avg = team_stats.get(a_team, 2.5)
                
                # ΕΦΑΡΜΟΓΗ POISSON
                p_over, p_gg, mu = calculate_tips(h_avg, a_avg)
                start_time = match_gr.strftime('%H:%M')
                league = m['competition']['name']

                if mu > 2.8:
                    t1, p1, t2, p2 = "Over 2.5", f"{p_over}%", "Goal-Goal", f"{p_gg}%"
                elif mu < 2.2:
                    t1, p1, t2, p2 = "Under 3.5", f"{95-p_over}%", "2-3 Goals", "68%"
                else:
                    t1, p1, t2, p2 = "1X & Over 1.5", f"{p_over+15}%", "Goal-Goal", f"{p_gg-5}%"

                output += f"{league} ({start_time})|{h_team} - {a_team}|{t1},{p1},{t2},{p2}\n"
        
        with open("daily_predictions.txt", "w", encoding="utf-8") as f:
            f.write(output)
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__":
    run()
