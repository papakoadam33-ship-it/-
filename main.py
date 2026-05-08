import requests
from datetime import datetime

def run():
    # Χρησιμοποιούμε το API που είδαμε ότι δουλεύει στην οθόνη σου
    url = "https://api.football-data.org/v4/matches"
    headers = { 'X-Auth-Token': 'a1a4edf072dc4b2c8153fced44c88de9' }
    
    all_content = f"🚀 MARIOS PRO AI TIPS\n"
    all_content += f"Ενημέρωση: {datetime.now().strftime('%d/%m %H:%M')}\n"
    all_content += "="*30 + "\n\n"
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        if 'matches' in data and data['matches']:
            for m in data['matches'][:15]: # Παίρνουμε τους 15 πιο κοντινούς αγώνες
                home = m['homeTeam']['name']
                away = m['awayTeam']['name']
                league = m['competition']['name']
                
                # Έξυπνος αλγόριθμος για Tips (αντί για σκέτο Over 1.5)
                # Εδώ μπορείς να προσθέσεις δική σου λογική
                tip = "1X & Over 1.5" 
                if "Cup" in league or "Libertadores" in league:
                    tip = "Goal-Goal"
                elif "Premier League" in league:
                    tip = "Over 2.5"
                
                all_content += f"🏆 {league}\n⚽ {home} - {away}\n➔ Προγνωστικό: {tip}\n"
                all_content += "-"*20 + "\n"
        else:
            all_content += "📅 Δεν υπάρχουν προγραμματισμένοι αγώνες για σήμερα."
            
    except Exception as e:
        all_content += f"❌ Σφάλμα: {str(e)}"

    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        f.write(all_content)

if __name__ == "__main__":
    run()

