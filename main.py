import requests
import time
from datetime import datetime, timedelta

# Το κλειδί σου
API_KEY = "47d5da2fb8mshde110deccc94426p115d5ajsnd9cc939fa561"

LEAGUE_IDS = [39, 140, 135, 71, 128, 94, 197]

def get_smart_tip(home_name, away_name):
    combined = len(home_name) + len(away_name)
    if combined % 4 == 0: return "Goal-Goal"
    if combined % 4 == 1: return "1X & Over 1.5"
    if combined % 4 == 2: return "Over 2.5"
    return "2-3 Goals"

def get_predictions():
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }
    
    today = datetime.now().strftime('%Y-%m-%d')
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    all_content = f"📅 Marios Pro Tips\nΕνημέρωση: {datetime.now().strftime('%d/%m %H:%M')}\n\n"
    found_any = False

    for league_id in LEAGUE_IDS:
        params = {"league": str(league_id), "next": "10"}
        try:
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                matches = data.get('response', [])
                if matches:
                    league_name = matches[0]['league']['name']
                    league_content = f"--- {league_name} ---\n"
                    has_m = False
                    for m in matches:
                        m_date = m['fixture']['date'][:10]
                        if m_date == today or m_date == tomorrow:
                            home = m['teams']['home']['name']
                            away = m['teams']['away']['name']
                            day = "Σήμερα" if m_date == today else "Αύριο"
                            tip = get_smart_tip(home, away)
                            league_content += f"⚽ [{day}] {home} vs {away} -> {tip}\n"
                            has_m = True
                            found_any = True
                    if has_m:
                        all_content += league_content + "\n"
            
            # ΠΡΟΣΘΗΚΗ ΚΑΘΥΣΤΕΡΗΣΗΣ (Για να αποφύγουμε το 429)
            time.sleep(2) 

        except Exception as e:
            print(f"Error: {e}")

    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        f.write(all_content if found_any else "Δεν βρέθηκαν αγώνες. Βεβαιώσου ότι έκανες Subscribe στο RapidAPI.")

if __name__ == "__main__":
    get_predictions()

