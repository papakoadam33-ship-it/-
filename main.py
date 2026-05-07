import requests
import time
from datetime import datetime, timedelta

API_KEY = "47d5da2fb8mshde110deccc94426p115d5ajsnd9cc939fa561"
HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

# Η λίστα σου με τα πρωταθλήματα
LEAGUE_IDS = [
    39, 40, 140, 141, 135, 136, 78, 81, 61, 94, 
    197, 198, 233, 71, 72, 128, 129, 
    2, 3, 848, 5, 10, 88, 144, 119
]

def get_real_prediction(fixture_id):
    """Φέρνει την πραγματική ανάλυση από το API-Football"""
    url = "https://api-football-v1.p.rapidapi.com/v3/predictions"
    try:
        # Μικρή αναμονή πριν από κάθε έξτρα call για προγνωστικό
        time.sleep(1) 
        response = requests.get(url, headers=HEADERS, params={"fixture": fixture_id})
        if response.status_code == 200:
            p_data = response.json()
            if p_data['response']:
                return p_data['response'][0]['predictions']['advice']
        return "2-3 Goals (Default)" # Backup αν δεν υπάρχει ανάλυση
    except:
        return "No Tip"

def run_marios_pro_tips():
    fixtures_url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    
    # Ημερομηνίες για τις επόμενες 3 ημέρες (για να είναι πιο γρήγορο)
    from_date = datetime.now().strftime('%Y-%m-%d')
    to_date = (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d')
    
    all_content = f"🚀 MARIOS PRO AI TIPS\nΕνημέρωση: {datetime.now().strftime('%d/%m %H:%M')}\n"
    all_content += "="*30 + "\n\n"
    
    found_any = False

    for lid in LEAGUE_IDS:
        params = {"league": str(lid), "from": from_date, "to": to_date}
        try:
            print(f"Ελέγχω το League ID: {lid}...")
            response = requests.get(fixtures_url, headers=HEADERS, params=params)
            
            if response.status_code == 200:
                matches = response.json().get('response', [])
                if matches:
                    league_info = f"🏆 {matches[0]['league']['name']} ({matches[0]['league']['country']})\n"
                    league_has_tips = False
                    
                    # Παίρνουμε τους 3 πιο σημαντικούς αγώνες για να μη κολλάει
                    for m in matches[:3]:
                        h, a = m['teams']['home']['name'], m['teams']['away']['name']
                        f_id = m['fixture']['id']
                        raw_date = m['fixture']['date']
                        m_date = raw_date[8:10] + "/" + raw_date[5:7]
                        
                        # ΕΔΩ ΓΙΝΕΤΑΙ Η ΜΑΓΕΙΑ: Πραγματικό Tip
                        tip = get_real_prediction(f_id)
                        
                        league_info += f"⚽ [{m_date}] {h} - {a} ➔ {tip}\n"
                        league_has_tips = True
                        found_any = True
                    
                    if league_has_tips:
                        all_content += league_info + "-"*20 + "\n"
            
            # Αναμονή 2 δευτερόλεπτα μεταξύ των πρωταθλημάτων
            time.sleep(2)
            
        except Exception as e:
            print(f"Error on league {lid}: {e}")

    # Αποθήκευση στο αρχείο για το GitHub Actions ή Streamlit
    filename = "daily_predictions.txt"
    with open(filename, "w", encoding="utf-8") as f:
        if found_any:
            f.write(all_content)
        else:
            f.write("Δεν βρέθηκαν αγώνες για το επόμενο τριήμερο.")
    
    print(f"✅ Ολοκληρώθηκε! Το αρχείο {filename} δημιουργήθηκε.")

if __name__ == "__main__":
    run_marios_pro_tips()
