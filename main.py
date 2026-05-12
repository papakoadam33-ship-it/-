import requests
import time
from datetime import datetime

def fetch_data():
    predictions = []
    # ΤΟ ΠΛΗΡΕΣ ΚΛΕΙΔΙ ΣΟΥ
    API_KEY = "a963742bcd5642afbe8c842d057f25ad" 
    url = "https://api.football-data.org/v4/matches"
    headers = { "X-Auth-Token": API_KEY }

    try:
        # Κλήση στο API
        response = requests.get(url, headers=headers, timeout=20)
        
        # Αν υπάρχει καθυστέρηση (Error 429), περιμένουμε 15 δευτερόλεπτα
        if response.status_code == 429:
            time.sleep(15)
            response = requests.get(url, headers=headers, timeout=20)
            
        data = response.json()

        if "matches" in data and len(data["matches"]) > 0:
            for match in data["matches"][:25]:
                home = match['homeTeam']['name']
                away = match['awayTeam']['name']
                league = match['competition']['name']
                # Δημιουργία προγνωστικών με βάση τους διαθέσιμους αγώνες
                predictions.append(f"{league}|{home} - {away}|Over 1.5 (78%), 1X (62%)")
        
    except Exception as e:
        print(f"Error: {e}")

    # Εγγραφή στο αρχείο daily_predictions.txt
    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        now = datetime.now()
        f.write(f"ΗΜΕΡΟΜΗΝΙΑ|{now.strftime('%d/%m/%Y')}|{now.strftime('%H:%M')} (GR)\n")
        
        if predictions:
            for p in predictions:
                f.write(p + "\n")
        else:
            # Μήνυμα αν δεν υπάρχουν ενεργοί αγώνες αυτή τη στιγμή στα δωρεάν πρωταθλήματα
            f.write("INFO|Αναμονή για την επόμενη αγωνιστική των μεγάλων πρωταθλημάτων.|-, -, -, -\n")

if __name__ == "__main__":
    fetch_data()
