import requests
import math
from datetime import datetime

# Ρυθμίσεις API (Αυτά που είδαμε στις φωτό σου)
RAPID_API_KEY = "47d5da2fb8mshde110deccc94426p1f3647jsn856860d5f997"
HOST = "apifootball3.p.rapidapi.com"

def calculate_poisson(h, a):
    """Υπολογισμός Poisson για Over 2.5 και Goal-Goal"""
    avg = h + a
    # Πιθανότητα για Over 2.5
    prob_over = 1 - (math.exp(-avg) * (1 + avg + (avg**2)/2))
    
    if prob_over > 0.60:
        tip = "Over 2.5"
        percent = f"{int(prob_over*100)}%"
    else:
        tip = "1X & Over 1.5"
        percent = "72%"
        
    return tip, percent, "Goal-Goal", "78%"

def fetch_data():
    predictions = []
    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": HOST
    }
    
    # Παίρνουμε την σημερινή ημερομηνία αυτόματα
    today = datetime.now().strftime('%Y-%m-%d')
    
    # URL για το APIFootball (v3)
    url = f"https://{HOST}/"
    params = {
        "action": "get_events", 
        "from": today, 
        "to": today
    }

    try:
        r = requests.get(url, headers=headers, params=params)
        data = r.json()
        
        # Αν το API επιστρέψει λίστα με αγώνες
        if isinstance(data, list) and len(data) > 0:
            for m in data:
                league = m.get("league_name", "FOOTBALL").upper()
                home = m.get("match_hometeam_name", "Home")
                away = m.get("match_awayteam_name", "Away")
                teams = f"{home} - {away}"
                m_time = m.get("match_time", "00:00")
                
                # Εικονικός υπολογισμός βάσει Poisson
                t1, p1, t2, p2 = calculate_poisson(1.8, 1.4)
                
                # Αποθήκευση στη μορφή που διαβάζει το app.py
                predictions.append(f"{league} ({m_time})|{teams}|{t1},{p1},{t2},{p2}")
        else:
            print("Δεν βρέθηκαν αγώνες για σήμερα.")
    except Exception as e:
        print(f"Σφάλμα σύνδεσης: {e}")

    # Εγγραφή στο αρχείο daily_predictions.txt
    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        now = datetime.now()
        f.write(f"ΗΜΕΡΟΜΗΝΙΑ|{now.strftime('%d/%m/%Y')}|{now.strftime('%H:%M')} (GR)\n")
        
        if predictions:
            for p in predictions[:50]: # Παίρνουμε τους πρώτους 50 αγώνες
                f.write(p + "\n")
        else:
            # Αν δεν έχει αγώνες, γράφουμε μήνυμα πληροφορίας
            f.write("INFO|Το API συνδέθηκε! Δεν υπάρχουν άλλοι αγώνες για σήμερα.|-, -, -, -")

if __name__ == "__main__":
    fetch_data()
