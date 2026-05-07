import requests
import time
from datetime import datetime

API_KEY = "47d5da2fb8mshde110deccc94426p115d5ajsnd9cc939fa561"

def test_api():
    # Δοκιμάζουμε να πάρουμε απλά τη λίστα με τις χώρες για να δούμε αν απαντάει
    url = "https://api-football-v1.p.rapidapi.com/v3/countries"
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        if response.status_code == 200 and data.get('response'):
            countries = [c['name'] for c in data['response'][:10]] # Παίρνουμε τις πρώτες 10 χώρες
            result = "Το API δουλεύει! Βρήκα αυτές τις χώρες: " + ", ".join(countries)
        else:
            result = f"Το API απάντησε αλλά είναι άδειο. Μήνυμα: {data.get('message', 'No message')}"
            
    except Exception as e:
        result = f"Σφάλμα σύνδεσης: {e}"

    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        f.write(result)

if __name__ == "__main__":
    test_api()

