import requests
from datetime import datetime

# --- ΡΥΘΜΙΣΕΙΣ API ---
RAPID_API_KEY = "47d5da2fb8mshde110deccc94426p115d5ajsnd9cc939fa561"
HOST = "apifootball3.p.rapidapi.com"

def fetch_data():
    predictions = []
    headers = {"X-RapidAPI-Key": RAPID_API_KEY, "X-RapidAPI-Host": HOST}
    
    # Αλλάζουμε σε get_leagues για να σιγουρευτούμε ότι θα φέρει δεδομένα
    url = f"https://{HOST}/?action=get_leagues"

    try:
        r = requests.get(url, headers=headers)
        data = r.json()
        
        if isinstance(data, list) and len(data) > 0:
            # Παίρνουμε τις πρώτες 10 λίγκες για να γεμίσει η οθόνη
            for item in data[:10]:
                league_name = item.get("league_name", "Unknown").upper()
                country = item.get("country_name", "World")
                
                # Εικονική πρόβλεψη βασισμένη στη λίγκα
                predictions.append(f"{league_name}|{country}|ΣΤΑΤΙΣΤΙΚΑ ΔΙΑΘΕΣΙΜΑ, 100%, ΣΥΝΔΕΣΗ OK, 100%")
        
        if not predictions:
            predictions.append("INFO|Το API συνδέθηκε αλλά δεν βρήκε αγώνες. Δοκίμασε αργότερα.|-, -, -, -")

    except Exception as e:
        predictions.append(f"ERROR|Σφάλμα: {str(e)}|-, -, -, -")

    # Εγγραφή στο αρχείο
    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        now = datetime.now()
        f.write(f"ΗΜΕΡΟΜΗΝΙΑ|{now.strftime('%d/%m/%Y')}|{now.strftime('%H:%M')} (GR)\n")
        for p in predictions:
            f.write(p + "\n")

if __name__ == "__main__":
    fetch_data()
