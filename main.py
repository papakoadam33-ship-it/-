import requests
import math
from datetime import datetime, timedelta

def poisson_probability(lmbda, x):
    return (math.exp(-lmbda) * (lmbda**x)) / math.factorial(x)

def calculate_tips(h_avg, a_avg):
    mu = (h_avg + a_avg) / 2
    p0 = poisson_probability(mu, 0)
    p1 = poisson_probability(mu, 1)
    p2 = poisson_probability(mu, 2)
    
    prob_over = (1 - (p0 + p1 + p2)) * 100
    # Πιο "επαγγελματικός" υπολογισμός GG (1 - πιθανότητα να μη σκοράρει ο ένας ή ο άλλος)
    prob_gg = (1 - math.exp(-h_avg/2)) * (1 - math.exp(-a_avg/2)) * 100
    
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
                        # Κρατάμε και τη φόρμα (π.χ. W,D,L,W,W)
                        form = row.get('form', 'N/A')
                        stats[team] = {'avg': avg, 'form': form}
        except: continue
    return stats

def run():
    headers = { 'X-Auth-Token': 'a1a4edf072dc4b2c8153fced44c88de9' }
    team_data = get_stats(headers)
    url = "https://api.football-data.org/v4/matches"
    
    try:
        data = requests.get(url, headers=headers).json()
        now_gr = datetime.utcnow() + timedelta(hours=3)
        output = f"ΗΜΕΡΟΜΗΝΙΑ|{now_gr.strftime('%d/%m/%Y')}|{now_gr.strftime('%H:%M')}\n"
        output += "ΛΙΓΚΑ | ΑΓΩΝΑΣ | ΠΡΟΒΛΕΨΗ | ΦΟΡΜΑ (H vs A)\n"
        output += "-"*80 + "\n"
        
        for m in data.get('matches', []):
            match_utc = datetime.strptime(m['utcDate'], '%Y-%m-%dT%H:%M:%SZ')
            match_gr = match_utc + timedelta(hours=3)
            
            if match_gr > now_gr:
                h_name, a_name = m['homeTeam']['name'], m['awayTeam']['name']
                
                # Λήψη δεδομένων με default τιμές αν δεν βρεθεί η ομάδα
                h_info = team_data.get(h_name, {'avg': 2.5, 'form': '???'})
                a_info = team_data.get(a_name, {'avg': 2.5, 'form': '???'})
                
                p_over, p_gg, mu = calculate_tips(h_info['avg'], a_info['avg'])
                start_time = match_gr.strftime('%H:%M')
                league = m['competition']['name']

                # Λογική επιλογής σημείου
                if mu > 2.9:
                    t1, p1 = "Over 2.5", f"{p_over}%"
                elif mu < 2.1:
                    t1, p1 = "Under 2.5", f"{100-p_over}%"
                else:
                    t1, p1 = "G/G ή 2-3", f"{p_gg}%"

                output += f"{league[:3]} ({start_time}) | {h_name} - {a_name} | {t1} ({p1}) | [{h_info['form']}] vs [{a_info['form']}]\n"
        
        print(output) # Το δείχνουμε και στην κονσόλα
        with open("daily_predictions.txt", "w", encoding="utf-8") as f:
            f.write(output)
            
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__":
    run()
