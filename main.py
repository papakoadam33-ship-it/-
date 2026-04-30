import requests

# ΑΝΤΙΚΑΤΑΣΤΗΣΕ ΤΟ "YOUR_API_KEY" ΜΕ ΤΟ ΚΛΕΙΔΙ ΣΟΥ ΑΠΟ ΤΟ API-FOOTBALL
API_KEY = "a963742bcd5642afbe8c842d057f25ad"
BASE_URL = "https://v3.football.api-sports.io/"

headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': API_KEY
}

# Λίστα με τα IDs των μεγάλων πρωταθλημάτων
LEAGUES = {
    'Ελλάδα (Super League)': 197,
    'Αγγλία (Premier League)': 39,
    'Ισπανία (La Liga)': 140,
    'Ιταλία (Serie A)': 135,
    'Γερμανία (Bundesliga)': 78,
    'Γαλλία (Ligue 1)': 61
}

def get_predictions():
    print("--- ΠΡΟΓΝΩΣΤΙΚΑ ΗΜΕΡΑΣ ---")
    for name, league_id in LEAGUES.items():
        url = f"{BASE_URL}fixtures?league={league_id}&next=5"
        response = requests.get(url, headers=headers)
        data = response.json()
        
        print(f"\nΠρωτάθλημα: {name}")
        if 'response' in data:
            for item in data['response']:
                home = item['teams']['home']['name']
                away = item['teams']['away']['name']
                date = item['fixture']['date'][:10]
                # Εδώ βάζεις έναν απλό κανόνα (π.χ. πρόβλεψη Over 1.5)
                print(f"[{date}] {home} vs {away} -> Πρόβλεψη: Over 1.5")

if __name__ == "__main__":
    if API_KEY == "YOUR_API_KEY":
        print("Πρέπει να βάλεις το API Key σου στο αρχείο!")
    else:
        get_predictions()
