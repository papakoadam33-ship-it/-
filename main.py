import requests
from datetime import datetime

# Χρησιμοποιούμε ένα δημόσιο API για έλεγχο
def run():
    url = "https://api.football-data.org/v4/matches"
    headers = { 'X-Auth-Token': 'a1a4edf072dc4b2c8153fced44c88de9' } # Προσωρινό κλειδί ελέγχου
    
    all_content = f"⚽ MARIOS DEBUG MODE\n"
    all_content += f"Ώρα Ελέγχου: {datetime.now().strftime('%d/%m %H:%M')}\n"
    all_content += "="*30 + "\n\n"
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        if 'matches' in data and data['matches']:
            all_content += "✅ Το API λειτουργεί! Βρέθηκαν αγώνες:\n\n"
            for m in data['matches'][:10]: # Παίρνουμε τους πρώτους 10 αγώνες
                home = m['homeTeam']['name']
                away = m['awayTeam']['name']
                league = m['competition']['name']
                all_content += f"🏆 {league}\n🔹 {home} - {away} ➔ Over 1.5\n\n"
        else:
            all_content += "❌ Το API απάντησε αλλά δεν βρήκε αγώνες."
            
    except Exception as e:
        all_content += f"❌ Σφάλμα σύνδεσης: {str(e)}"

    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        f.write(all_content)

if __name__ == "__main__":
    run()
