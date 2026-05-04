import requests
import os

# Βάλε το κλειδί σου εδώ
API_KEY = "a1a4edf072dc4b2c8153fced44c88de9"

def get_predictions():
    # Στο Free Tier έχουμε πρόσβαση σε συγκεκριμένα πρωταθλήματα (π.χ. PL, CL, BL1, SA, PD, FL1)
    # Θα πάρουμε τα ματς των επόμενων 7 ημερών για να είμαστε σίγουροι
    url = "https://api.football-data.org/v4/matches"
    headers = { 'X-Auth-Token': API_KEY }
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 429:
            print("Σφάλμα: Πολλά αιτήματα (Rate Limit). Περίμενε ένα λεπτό.")
            return
            
        data = response.json()

        with open("daily_predictions.txt", "w", encoding="utf-8") as f:
            f.write("=== ΠΡΟΓΝΩΣΤΙΚΑ ΗΜΕΡΑΣ ===\n\n")
            
            if 'matches' in data and len(data['matches']) > 0:
                for match in data['matches']:
                    home = match['homeTeam']['name']
                    away = match['awayTeam']['name']
                    league = match['competition']['name']
                    
                    line = f"[{league}] {home} vs {away} -> Προγνωστικό: Over 1.5\n"
                    f.write(line)
                print("Τα προγνωστικά γράφτηκαν στο αρχείο.")
            else:
                f.write("Δεν βρέθηκαν προγραμματισμένοι αγώνες για τα διαθέσιμα πρωταθλήματα σήμερα.\n")
                print("Δεν βρέθηκαν αγώνες.")
                
    except Exception as e:
        print(f"Κάτι πήγε στραβά: {e}")

if __name__ == "__main__":
    get_predictions()
