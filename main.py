import requests
from datetime import datetime, timedelta

def get_stats(headers):
    # Παίρνουμε τη βαθμολογία για τις κύριες λίγκες για να έχουμε δεδομένα γκολ
    leagues = ['PL', 'PD', 'BL1', 'SA', 'FL1', 'ELC']
    stats = {}
    for league in leagues:
        try:
            url = f"https://api.football-data.org/v4/competitions/{league}/standings"
            res = requests.get(url, headers=headers).json()
            if 'standings' in res:
                for row in res['standings'][0]['table']:
                    team_name = row['team']['name']
                    matches = row['playedGames']
                    goals_for = row['goalsFor']
                    goals_against = row['goalsAgainst']
                    # Μέσος όρος γκολ ανά αγώνα (Επίθεση + Άμυνα)
                    avg = (goals_for + goals_against) / matches if matches > 0 else 0
                    stats[team_name] = round(avg, 2)
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
            if m['status'] in ['TIMED', 'SCHEDULED']:
                league = m['competition']['name']
                h_team = m['homeTeam']['name']
                a_team = m['awayTeam']['name']
                
                # Υπολογισμός "Δύναμης Γκολ" (Goal Power)
                h_avg = team_stats.get(h_team, 2.5) # Αν δεν υπάρχει data, βάζουμε 2.5 μ.ο.
                a_avg = team_stats.get(a_team, 2.5)
                total_power = (h_avg + a_avg) / 2
                
                # Πραγματικά Ποσοστά βάσει Goal Power
                prob_over = int(min(total_power * 25, 92)) # max 92%
                prob_gg = int(min(total_power * 22, 88))
                
                l_up = league.upper()
                if total_power > 3.0:
                    t1, p1, t2, p2 = "Over 2.5", f"{prob_over}%", "Goal-Goal", f"{prob_gg}%"
                elif total_power < 2.2:
                    t1, p1, t2, p2 = "Under 3.5", f"{int(100-prob_over+20)}%", "2-3 Goals", "65%"
                else:
                    t1, p1, t2, p2 = "1X & Over 1.5", f"{prob_over-5}%", "Goal-Goal", f"{prob_gg-5}%"

                output += f"{league}|{h_team} - {a_team}|{t1},{p1},{t2},{p2}\n"
        
        with open("daily_predictions.txt", "w", encoding="utf-8") as f:
            f.write(output)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run()
