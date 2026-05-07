import requests
import time
from datetime import datetime, timedelta

# Ρυθμίσεις API
API_KEY = "47d5da2fb8mshde110deccc94426p115d5ajsnd9cc939fa561"
HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

# Διευρυμένη λίστα πρωταθλημάτων
LEAGUE_IDS = [
    39, 40, 140, 141, 135, 136, 78, 81, 61, 94, 
    197, 198, 233, 71, 72, 128, 129, 
    2, 3, 848, 5, 10, 88, 144, 119
]

def get_real_prediction(fixture_id):
    url = "https://api-football-v1.p.rapidapi.com/v3/predictions"
    try:
        time.sleep(1.5) # Καθυστέρηση για το Rate Limit
        response = requests.get(url, headers=HEADERS, params={"fixture": fixture_id})
        if response.status_code == 200:
            p_data = response.json()
            if p_data['response']:
                return p_data['response'][0]['predictions']['advice']
        return "2-3 Goals"
    except:
        return "No Tip Available"

def run_script():
    fixtures_url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    
    # Ψάχνουμε για τις επόμενες 7 ημέρες για να έχουμε πάντα περιεχόμενο
    from_date = datetime.now().strftime('%Y-%m-%d')
    to_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
    
    all_content = f"🚀 MARIOS PRO AI TIPS\n"
    all_content += f"Τελευταία Ενημέρωση: {datetime.now().strftime('%d/%m %H:%M')}\n"
    all_content += "="*30 + "\n\n"
    
    found_any = False

    for lid in LEAGUE_IDS:
        params = {"league": str(lid), "from": from_date, "to": to_date}
        try:
            response = requests.get(fixtures_url, headers=HEADERS, params=params)
            if response.status_code == 200:
                matches = response.json().get('response', [])
                if matches:
                    league_name = matches[0]['league']['name']
                    all_content += f"🏆 {league_name}\n"
                    
                    # Παίρνουμε έως 5 αγώνες ανά πρωτάθλημα
                    for m in matches[:5]:
                        h, a = m['teams']['home']['name'], m['teams']['away']['name']
                        f_id = m['fixture']['id']
                        raw_date = m['fixture']['date']
                        m_date = raw_date[8:10] + "/" + raw_date[5:7]
                        
                        tip = get_real_prediction(f_id)
                        all_content += f"⚽ [{m_date}] {h} - {a} ➔ {tip}\n"
                        found_any = True
                    all_content += "-"*20 + "\n\n"
            
            time.sleep(2) # Αναμονή μεταξύ πρωταθλημάτων
            
        except Exception as e:
            print(f"Error: {e}")

    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        if found_any:
            f.write(all_content)
        else:
            f.write("📅 Δεν βρέθηκαν προγραμματισμένοι αγώνες για την επόμενη εβδομάδα.")

if __name__ == "__main__":
    run_script()

