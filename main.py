import requests
from datetime import datetime, timedelta

# --- ΡΥΘΜΙΣΕΙΣ API ---
# Χρησιμοποιούμε το κλειδί σου που είναι ήδη ενεργοποιημένο στο BASIC
RAPID_API_KEY = "47d5da2fb8mshde110deccc94426p115d5ajsnd9cc939fa561"
HOST = "apifootball3.p.rapidapi.com"

def calculate_poisson(h, a):
    """Υπολογισμός εικονικής πρόβλεψης"""
    return "Over 2.5", "78%", "Goal-Goal", "72%"

def fetch_data():
    predictions = []
    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": HOST
    }
    
    # Ρύθμιση ημερομηνιών: Από σήμερα έως +3 ημέρες για να βρούμε σίγουρα αγώνες
    start_date = datetime.now().strftime('%Y-%m-%d')
    end_date = (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d')
    
    url = f"https://{HOST}/"
    params = {
        "action": "get_events",
        "from": start_date,
        "to": end_date,
        "timezone": "Europe/Athens"
    }

    try:
        r = requests.get(url, headers=headers, params=params)
        data = r.json()
        
        # Έλεγχος αν το API επέστρεψε λίστα
        if isinstance(data, list) and len(data) > 0:
            for item in data:
                league = item.get("league_name", "Unknown League").upper()
                home = item.get("match_hometeam_name", "Home")
                away = item.get("match_awayteam_name", "Away")
                m_date = item.get("match_date", "")
                m_time = item.get("match_time", "00:00")
                
                teams = f"{home} - {away}"
                t1, p1, t2, p2 = calculate_poisson(1.5, 1.3)
                
                # Εμφανίζουμε και την ημερομηνία για να ξέρουμε πότε είναι το ματς
                predictions.append(f"{league} ({m_date} {m_time})|{teams}|{t1},{p1},{t2},{p2}")
        
        if not predictions:
            predictions.append("INFO|Το API είναι ONLINE αλλά δεν βρέθηκαν αγώνες για το επόμενο 3ήμερο στο BASIC πακέτο.|-, -, -, -")

    except Exception as e:
        predictions.append(f"ERROR|Σφάλμα Σύνδεσης: {str(e)}|-, -, -, -")

    # Εγγραφή στο αρχείο daily_predictions.txt
    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        now = datetime.now()
        f.write(f"ΗΜΕΡΟΜΗΝΙΑ|{now.strftime('%d/%m/%Y')}|{now.strftime('%H:%M')} (GR)\n")
        for p in predictions[:50]: # Παίρνουμε τους πρώτους 50 αγώνες
            f.write(p + "\n")

if __name__ == "__main__":
    fetch_data()
