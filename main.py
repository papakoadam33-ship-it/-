
import requests

API_KEY = "ΤΟ_ΚΛΕΙΔΙ_ΣΟΥ_ΕΔΩ"

# Λίστα με τα πρωταθλήματα που θέλουμε να ελέγχουμε
LEAGUES = {
    'Premier League': 'PL',
    'La Liga': 'PD',
    'Serie A': 'SA',
    'Bundesliga': 'BL1',
    'Ligue 1': 'FL1',
    'Champions League': 'CL',
    'Copa Libertadores': 'CLI'
}

def get_predictions():
    headers = { 'X-Auth-Token': API_KEY }
    all_content = ""
    
    for league_name, league_code in LEAGUES.items():
        # Ζητάμε μόνο τα προγραμματισμένα ματς (SCHEDULED)
        url = f"https://api.football-data.org/v4/competitions/{league_code}/matches?status=SCHEDULED"
        
        try:
            response = requests.get(url, headers=headers)
            data = response.json()
            
            matches_list = []
            if 'matches' in data:
                # Παίρνουμε μόνο τα επόμενα 3 ματς από κάθε πρωτάθλημα για να μην γεμίζει η οθόνη
                for match in data['matches'][:3]:
                    home = match.get('homeTeam', {}).get('name')
                    away = match.get('awayTeam', {}).get('name')
                    date = match.get('utcDate', '')[:10]
                    
                    # ΕΛΕΓΧΟΣ: Πρόσθεσε το ματς ΜΟΝΟ αν υπάρχουν ονόματα ομάδων
                    if home and away and home != "None" and away != "None":
                        matches_list.append(f"[{date}] {home} vs {away} -> Προγνωστικό: Over 1.5")
            
            if matches_list:
                all_content += f"--- {league_name} ---\n"
                for m in matches_list:
                    all_content += m + "\n"
                all_content += "\n"
                
        except Exception as e:
            print(f"Error in {league_name}: {e}")

    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        if all_content:
            f.write(all_content)
        else:
            f.write("Δεν βρέθηκαν διαθέσιμοι αγώνες για σήμερα.")

if __name__ == "__main__":
    get_predictions()
