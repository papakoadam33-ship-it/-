import requests
from datetime import datetime

def run():
    # Ρυθμίσεις API
    url = "https://api.football-data.org/v4/matches"
    headers = { 'X-Auth-Token': 'a1a4edf072dc4b2c8153fced44c88de9' }
    
    # Προετοιμασία ημερομηνίας και ώρας για την κορυφή της εφαρμογής
    now = datetime.now()
    date_str = now.strftime('%d/%m/%Y')
    time_str = now.strftime('%H:%M')
    
    # Η πρώτη γραμμή χρησιμοποιεί το σύμβολο | για να την ξεχωρίζει το app.py
    output = f"ΗΜΕΡΟΜΗΝΙΑ|{date_str}|{time_str}\n"
    
    try:
        # Λήψη δεδομένων
        response = requests.get(url, headers=headers)
        data = response.json()
        
        if 'matches' in data:
            # Παίρνουμε έως 40 αγώνες για να γεμίσει η σελίδα
            for m in data['matches'][:40]:
                league = m['competition']['name']
                home = m['homeTeam']['name']
                away = m['awayTeam']['name']
                
                # --- ΑΛΓΟΡΙΘΜΟΣ ΕΞΥΠΝΩΝ ΠΡΟΓΝΩΣΤΙΚΩΝ ---
                l_up = league.upper()
                
                if "COPA LIBERTADORES" in l_up:
                    tip = "Goal-Goal"
                elif "BUNDESLIGA" in l_up or "LIGUE 1" in l_up:
                    tip = "Over 2.5"
                elif "CHAMPIONSHIP" in l_up or "SERIE A" in l_up:
                    tip = "2-3 Goals"
                elif "PREMIER LEAGUE" in l_up:
                    tip = "1 & Over 1.5"
                else:
                    tip = "1X & Over 1.5" # Βασικό προγνωστικό
                
                # Προσθήκη του αγώνα στο αρχείο με το διαχωριστικό |
                output += f"{league} | {home} - {away} | {tip}\n"
        else:
            output += "ΣΦΑΛΜΑ | Δεν βρέθηκαν αγώνες | -\n"
            
    except Exception as e:
        output += f"ΣΦΑΛΜΑ | Πρόβλημα API: {str(e)} | -\n"

    # Εγγραφή στο αρχείο daily_predictions.txt
    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        f.write(output)

if __name__ == "__main__":
    run()
