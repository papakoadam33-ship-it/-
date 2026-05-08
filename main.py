import requests
from datetime import datetime

def run():
    # Χρησιμοποιούμε το API που ξέρουμε ότι δουλεύει
    url = "https://api.football-data.org/v4/matches"
    headers = { 'X-Auth-Token': 'a1a4edf072dc4b2c8153fced44c88de9' }
    
    # Η πρώτη γραμμή είναι η ημερομηνία
    output = f"ΕΝΗΜΕΡΩΣΗ: {datetime.now().strftime('%d/%m %H:%M')}\n"
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        if 'matches' in data:
            # Παίρνουμε τους πρώτους 20 αγώνες για να έχεις γεμάτη οθόνη
            for m in data['matches'][:20]:
                league = m['competition']['name']
                home = m['homeTeam']['name']
                away = m['awayTeam']['name']
                
                # Χρησιμοποιούμε το σύμβολο | για να μη μπερδεύεται το app.py
                output += f"{league} | {home} - {away} | 1X & Over 1.5\n"
        else:
            output += "Δεν βρέθηκαν αγώνες για σήμερα.\n"
    except Exception as e:
        output += f"Σφάλμα API: {str(e)}\n"

    # Αποθήκευση στο αρχείο
    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        f.write(output)

if __name__ == "__main__":
    run()

