import requests
from datetime import datetime, timedelta

def run():
    url = "https://api.football-data.org/v4/matches"
    headers = { 'X-Auth-Token': 'a1a4edf072dc4b2c8153fced44c88de9' }
    
    now_gr = datetime.utcnow() + timedelta(hours=3)
    date_str = now_gr.strftime('%d/%m/%Y')
    time_str = now_gr.strftime('%H:%M')
    
    output = f"ΗΜΕΡΟΜΗΝΙΑ|{date_str}|{time_str}\n"
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        if 'matches' in data:
            count = 0
            for m in data['matches']:
                if m['status'] in ['TIMED', 'SCHEDULED']:
                    league = m['competition']['name']
                    home = m['homeTeam']['name']
                    away = m['awayTeam']['name']
                    
                    utc_time = datetime.strptime(m['utcDate'], '%Y-%m-%dT%H:%M:%SZ')
                    gr_time = utc_time + timedelta(hours=3)
                    start_time = gr_time.strftime('%H:%M')

                    l_up = league.upper()
                    
                    # ΔΙΠΛΕΣ ΠΡΟΤΑΣΕΙΣ ΑΝΑ ΛΙΓΚΑ
                    if "LIBERTADORES" in l_up:
                        tip1, tip2 = "Goal-Goal", "Over 2.5"
                    elif "BUNDESLIGA" in l_up or "LIGUE 1" in l_up:
                        tip1, tip2 = "Over 2.5", "Goal-Goal"
                    elif "SERIE A" in l_up or "CHAMPIONSHIP" in l_up:
                        tip1, tip2 = "2-3 Goals", "Under 3.5"
                    elif "PREMIER LEAGUE" in l_up or "LA LIGA" in l_up or "PRIMERA" in l_up:
                        tip1, tip2 = "1 & Over 1.5", "1X & Over 2.5"
                    else:
                        tip1, tip2 = "1X & Over 1.5", "Goal-Goal"
                    
                    # Τώρα σώζουμε και τα δύο tips χωρισμένα με κόμμα
                    output += f"{league} ({start_time}) | {home} - {away} | {tip1}, {tip2}\n"
                    count += 1
                if count >= 40: break
    except:
        output += "ΣΦΑΛΜΑ | Πρόβλημα API | -\n"

    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        f.write(output)

if __name__ == "__main__":
    run()
