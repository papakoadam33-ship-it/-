import requests
from datetime import datetime, timedelta

def run():
    url = "https://api.football-data.org/v4/matches"
    headers = { 'X-Auth-Token': 'a1a4edf072dc4b2c8153fced44c88de9' }
    
    now = datetime.now()
    date_str = now.strftime('%d/%m/%Y')
    time_str = now.strftime('%H:%M')
    
    output = f"ΗΜΕΡΟΜΗΝΙΑ|{date_str}|{time_str}\n"
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        if 'matches' in data:
            count = 0
            for m in data['matches']:
                # Μόνο αγώνες που δεν έχουν ξεκινήσει
                if m['status'] in ['TIMED', 'SCHEDULED']:
                    league = m['competition']['name']
                    home = m['homeTeam']['name']
                    away = m['awayTeam']['name']
                    
                    # Ώρα Ελλάδας (+3 ώρες από UTC)
                    utc_time = datetime.strptime(m['utcDate'], '%Y-%m-%dT%H:%M:%SZ')
                    gr_time = utc_time + timedelta(hours=3)
                    start_time = gr_time.strftime('%H:%M')

                    # Αλγόριθμος
                    l_up = league.upper()
                    if "COPA LIBERTADORES" in l_up: tip = "Goal-Goal"
                    elif "BUNDESLIGA" in l_up: tip = "Over 2.5"
                    elif "SERIE A" in l_up: tip = "2-3 Goals"
                    else: tip = "1X & Over 1.5"
                    
                    output += f"{league} ({start_time}) | {home} - {away} | {tip}\n"
                    count += 1
                if count >= 40: break
    except:
        output += "ΣΦΑΛΜΑ | Πρόβλημα σύνδεσης | -\n"

    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        f.write(output)

if __name__ == "__main__":
    run()
