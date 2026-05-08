import requests
from datetime import datetime

def run():
    # Το API URL και το Token σου
    url = "https://api.football-data.org/v4/matches"
    headers = { 'X-Auth-Token': 'a1a4edf072dc4b2c8153fced44c88de9' }
    
    # Η πρώτη γραμμή με την ημερομηνία ενημέρωσης
    output = f"ΕΝΗΜΕΡΩΣΗ: {datetime.now().strftime('%d/%m %H:%M')}\n"
    
    try:
        # Παίρνουμε τα δεδομένα από το API
        response = requests.get(url, headers=headers)
        data = response.json()
        
        if 'matches' in data:
            # Παίρνουμε έως 40 αγώνες για να είναι γεμάτη η εφαρμογή
            for m in data['matches'][:40]:
                league = m['competition']['name']
                home = m['homeTeam']['name']
                away = m['awayTeam']['name']
                
                # --- ΕΞΥΠΝΟΣ ΑΛΓΟΡΙΘΜΟΣ ΠΡΟΓΝΩΣΤΙΚΩΝ ---
                league_upper = league.upper()
                
                if "COPA LIBERTADORES" in league_upper:
                    tip = "Goal-Goal"
                elif "BUNDESLIGA" in league_upper or "LIGUE 1" in league_upper:
                    tip = "Over 2.5"
                elif "CHAMPIONSHIP" in league_upper or "SERIE A" in league_upper:
                    tip = "2-3 Goals"
                elif "PREMIER LEAGUE" in league_upper:
                    tip = "1 & Over 1.5"
                else:
                    # Το βασικό προγνωστικό για τα υπόλοιπα
                    tip = "1X & Over 1.5"
                
                # Δημιουργία της γραμμής με το διαχωριστικό |
                output += f"{league} | {home} - {away} | {tip}\n"
        else:
            output += "Δεν βρέθηκαν διαθέσιμοι αγώνες.\n"
            
    except Exception as e:
        output += f"Σφάλμα κατά τη λήψη: {str(e)}\n"

    # Αποθήκευση στο αρχείο που διαβάζει το app.py
    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        f.write(output)

if __name__ == "__main__":
    run()
