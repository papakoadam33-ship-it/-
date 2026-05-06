import requests
from datetime import datetime

# Βάλε εδώ το ΝΕΟ API Key από το api-sports.io
API_KEY = "ΤΟ_ΝΕΟ_ΣΟΥ_API_KEY"

# IDs πρωταθλημάτων για το API-Football:
# 135: Serie A (Italy), 39: Premier League, 140: La Liga, 71: Serie A (Brazil), 
# 128: Liga Profesional (Argentina), 94: Primeira Liga (Portugal)
LEAGUE_IDS = [39, 140, 135, 71, 128, 94]

def get_smart_tip(home_name, away_name):
    # Εδώ μπορούμε μελλοντικά να προσθέσουμε στατιστικά.
    # Προς το παρόν, ας χρησιμοποιήσουμε μια ποικιλία σημείων.
    name_sum = len(home_name) + len(away_name)
    if name_sum % 5 == 0: return "Goal-Goal"
    if name_sum % 5 == 1: return "1X & Over 1.5"
    if name_sum % 5 == 2: return "Over 2.5"
    if name_sum % 5 == 3: return "2-3 Goals"
    return "X2 & Under 4.5"

def get_predictions():
    url = "https://v3.football.api-sports.io/fixtures"
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': 'v3.football.api-sports.io'
    }
    
    all_content = f"📅 Προγνωστικά Marios Pro (API-Football)\nΕνημέρωση: {datetime.now().strftime('%d/%m %H:%M')}\n\n"
    found_any = False

    for league_id in LEAGUE_IDS:
        # Παίρνουμε τους επόμενους 5 αγώνες για κάθε πρωτάθλημα
        params = {'league': league_id, 'next': 5}
        
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                data = response.json()
                matches = data.get('response', [])
                
                if matches:
                    league_name = matches[0]['league']['name']
                    all_content += f"--- {league_name} ---\n"
                    
                    for m in matches:
                        home = m['teams']['home']['name']
                        away = m['teams']['away']['name']
                        # Μετατροπή ημερομηνίας
                        date_raw = m['fixture']['date'][:10]
                        date_obj = datetime.strptime(date_raw, '%Y-%m-%d')
                        date_final = date_obj.strftime('%d/%m')
                        
                        tip = get_smart_tip(home, away)
                        all_content += f"⚽ [{date_final}] {home} vs {away} -> {tip}\n"
                        found_any = True
                    all_content += "\n"
            
        except Exception as e:
            print(f"Error fetching league {league_id}: {e}")

    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        if found_any:
            f.write(all_content)
        else:
            f.write("Δεν βρέθηκαν αυριανοί αγώνες. Ελέγξτε το API Key.")

if __name__ == "__main__":
    get_predictions()

