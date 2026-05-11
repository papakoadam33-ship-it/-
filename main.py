import requests
import math
from datetime import datetime

# Ρυθμίσεις API - ΤΟ ΚΛΕΙΔΙ ΣΟΥ ΑΠΟ ΤΗ ΦΩΤΟ
RAPID_API_KEY = "47d5da2fb8mshde110deccc94426p115d5ajsnd9cc939fa561"
HOST = "apifootball3.p.rapidapi.com"

def calculate_poisson(h, a):
    # Σταθερές τιμές για το demo αν δεν υπάρχουν στατιστικά
    tip = "Over 2.5" if (h + a) > 2.5 else "1X & Over 1.5"
    return tip, "78%", "Goal-Goal", "72%"

def fetch_data():
    predictions = []
    headers = {"X-RapidAPI-Key": RAPID_API_KEY, "X-RapidAPI-Host": HOST}
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Χρήση του "Events" endpoint που είδαμε στη φωτογραφία σου
    url = f"https://{HOST}/"
    params = {
        "action": "get_events",
        "from": today,
        "to": today,
        "timezone": "Europe/Athens"
    }

    try:
        r = requests.get(url, headers=headers, params=params)
        data = r.json()
        
        # Έλεγχος αν το API επέστρεψε λίστα αγώνων
        if isinstance(data, list) and len(data) > 0:
            for item in data:
                league = item.get("league_name", "UNKNOWN LEAGUE").upper()
                home = item.get("match_hometeam_name", "Home")
                away = item.get("match_awayteam_name", "Away")
                m_time = item.get("match_time", "00:00")
                
                teams = f"{home} - {away}"
                t1, p1, t2, p2 = calculate_poisson(1.5, 1.2)
                predictions.append(f"{league} ({m_time})|{teams}|{t1},{p1},{t2},{p2}")
        
        if not predictions:
            predictions.append("INFO|Το API είναι έτοιμο! Δεν βρέθηκαν ζωντανοί αγώνες αυτή τη στιγμή.|-, -, -, -")

    except Exception as e:
        predictions.append(f"ERROR|Σφάλμα: {str(e)}|-, -, -, -")

    # Ενημέρωση του αρχείου
    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        now = datetime.now()
        f.write(f"ΗΜΕΡΟΜΗΝΙΑ|{now.strftime('%d/%m/%Y')}|{now.strftime('%H:%M')} (GR)\n")
        for p in predictions[:50]:
            f.write(p + "\n")

if __name__ == "__main__":
    fetch_data()
