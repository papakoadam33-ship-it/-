import requests
import os

# Βάλε το κλειδί σου εδώ μέσα στα εισαγωγικά
API_KEY = "ΤΟ_ΚΛΕΙΔΙ_ΣΟΥ_ΕΔΩ"

LEAGUES = {
    'Premier League': 'PL',
    'La Liga': 'PD',
    'Serie A': 'SA',
    'Bundesliga': 'BL1',
    'Ligue 1': 'FL1',
    'Champions League': 'CL'
}

def get_predictions():
    # Καθαρισμός κλειδιού από κρυφούς χαρακτήρες που προκαλούν το latin-1 error
    clean_key = str(API_KEY).strip()
    headers = { 'X-Auth-Token': clean_key }
    all_content = ""
    
    for league_name, league_code in LEAGUES.items():
        url = f"https://api.football-data.org/v4/competitions/{league_code}/matches?status=SCHEDULED"
        
        try:
            response = requests.get(url, headers=headers)
            # Έλεγχος αν το API απάντησε σωστά
            if response.status_code == 200:
                data = response.json()
                matches_list = []
                
                if 'matches' in data:
                    for match in data['matches'][:3]: # Τα 3 επόμενα ματς
                        home = match.get('homeTeam', {}).get('name')
                        away = match.get('awayTeam', {}).get('name')
                        date = match.get('utcDate', '')[:10]
                        
                        if home and away:
                            matches_list.append(f"[{date}] {home} vs {away} -> Προγνωστικό: Over 1.5")
                
                if matches_list:
                    all_content += f"--- {league_name} ---\n"
                    for m in matches_list:
                        all_content += m + "\n"
                    all_content += "\n"
            else:
                print(f"Σφάλμα στο {league_name}: Status {response.status_code}")
                
        except Exception as e:
            print(f"Σφάλμα σύνδεσης στο {league_name}: {e}")

    # Γράψιμο στο αρχείο με κωδικοποίηση utf-8 για τα Ελληνικά
    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        if all_content:
            f.write(all_content)
        else:
            f.write("Δεν βρέθηκαν διαθέσιμοι αγώνες προς το παρόν.")

if __name__ == "__main__":
    get_predictions()

