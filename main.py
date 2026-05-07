import requests
import time
from datetime import datetime, timedelta

# Το κλειδί σου (Ήδη μέσα)
API_KEY = "47d5da2fb8mshde110deccc94426p115d5ajsnd9cc939fa561"

# Λίστα με πολλά πρωταθλήματα για να μην μένει ποτέ άδεια η εφαρμογή
LEAGUE_IDS = [
    39, 40, 140, 141, 135, 136, 78, 81, 61, 94, # Αγγλία (1-2), Ισπανία (1-2), Ιταλία (1-2), Γερμανία, Πορτογαλία
    197, 198, 233, # Ελλάδα (Superleague 1 & 2), Κύπρος
    71, 72, 128, 129, # Βραζιλία, Αργεντινή
    2, 3, 848, 5, 10, # Champions League, Europa League, Conference League, Nations League, Προκριματικά Μουντιάλ
    88, 144, 119 # Ολλανδία, Βέλγιο, Δανία
]

def get_smart_tip(home, away):
    # Έξυπνη επιλογή προγνωστικού βάσει ονομάτων
    combined = len(home) + len(away)
    if combined % 4 == 0: return "1X & Over 1.5"
    if combined % 4 == 1: return "Goal-Goal"
    if combined % 4 == 2: return "Over 2.5"
    return "2-3 Goals"

def get_predictions():
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }
    
    # Ψάχνουμε αγώνες για τις επόμενες 5 ημέρες
    from_date = datetime.now().strftime('%Y-%m-%d')
    to_date = (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d')
    
    all_content = f"📅 Marios Pro Tips\nΤελευταία Ενημέρωση: {datetime.now().strftime('%H:%M')}\n\n"
    found_any = False

    for lid in LEAGUE_IDS:
        params = {"league": str(lid), "from": from_date, "to": to_date}
        try:
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                data = response.json()
                matches = data.get('response', [])
                if matches:
                    all_content += f"🏆 {matches[0]['league']['name']} ({matches[0]['league']['country']})\n"
                    # Παίρνουμε τους 4 πρώτους αγώνες από κάθε λίγκα
                    for m in matches[:4]:
                        h, a = m['teams']['home']['name'], m['teams']['away']['name']
                        # Μορφή ημερομηνίας ΗΗ/ΜΜ
                        raw_date = m['fixture']['date']
                        m_date = raw_date[8:10] + "/" + raw_date[5:7]
                        
                        tip = get_smart_tip(h, a)
                        all_content += f"⚽ [{m_date}] {h} - {a} ➔ {tip}\n"
                        found_any = True
                    all_content += "----------------------------\n\n"
            
            # 7 δευτερόλεπτα αναμονή για να μην φας μπλοκάρισμα (Rate Limit)
            time.sleep(7) 
            
        except Exception as e:
            print(f"Error on league {lid}: {e}")

    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        if found_any:
            f.write(all_content)
        else:
            f.write("Δεν βρέθηκαν αγώνες. Δοκίμασε ξανά σε λίγο.")

if __name__ == "__main__":
    get_predictions()

