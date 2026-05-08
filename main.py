import requests
from datetime import datetime, timedelta

def run():
    # Το API Key σου
    url = "https://api.football-data.org/v4/matches"
    headers = { 'X-Auth-Token': 'a1a4edf072dc4b2c8153fced44c88de9' }
    
    # Τρέχουσα ώρα Ελλάδας (UTC+3) για την κεφαλίδα της εφαρμογής
    now_gr = datetime.utcnow() + timedelta(hours=3)
    date_str = now_gr.strftime('%d/%m/%Y')
    time_str = now_gr.strftime('%H:%M')
    
    output = f"ΗΜΕΡΟΜΗΝΙΑ|{date_str}|{time_str}\n"
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        if 'matches' in data:
            count = 0
            for m in data['matches']:
                # ΦΙΛΤΡΟ: Μόνο αγώνες που ΔΕΝ έχουν ξεκινήσει
                if m['status'] in ['TIMED', 'SCHEDULED']:
                    league = m['competition']['name']
                    home = m['homeTeam']['name']
                    away = m['awayTeam']['name']
                    
                    # ΔΙΟΡΘΩΣΗ ΩΡΑΣ: Μετατροπή UTC σε ώρα Ελλάδας (+3 ώρες)
                    utc_time = datetime.strptime(m['utcDate'], '%Y-%m-%dT%H:%M:%SZ')
                    gr_time = utc_time + timedelta(hours=3)
                    start_time = gr_time.strftime('%H:%M')

                    # ΣΤΑΘΕΡΟΣ ΑΛΓΟΡΙΘΜΟΣ ΠΡΟΓΝΩΣΤΙΚΩΝ
                    # Χρησιμοποιούμε λέξεις-κλειδιά για να μην αλλάζει το σημείο ποτέ
                    l_up = league.upper()
                    
                    if "LIBERTADORES" in l_up:
                        tip = "Goal-Goal"
                    elif "BUNDESLIGA" in l_up or "LIGUE 1" in l_up:
                        tip = "Over 2.5"
                    elif "SERIE A" in l_up or "CHAMPIONSHIP" in l_up:
                        tip = "2-3 Goals"
                    elif "PREMIER LEAGUE" in l_up or "LA LIGA" in l_up or "PRIMERA" in l_up:
                        tip = "1 & Over 1.5"
                    else:
                        # Σταθερό σημείο για όλα τα υπόλοιπα πρωταθλήματα
                        tip = "1X & Over 1.5"
                    
                    # Αποθήκευση στη μορφή που διαβάζει το app.py
                    output += f"{league} ({start_time}) | {home} - {away} | {tip}\n"
                    count += 1
                
                # Εμφάνιση έως 40 αγώνων
                if count >= 40:
                    break
        
        if count == 0:
            output += "ΠΛΗΡΟΦΟΡΙΑ | Δεν υπάρχουν άλλοι αγώνες για σήμερα | -\n"
            
    except Exception as e:
        output += f"ΣΦΑΛΜΑ | Πρόβλημα API: {str(e)} | -\n"

    # Εγγραφή στο αρχείο daily_predictions.txt
    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        f.write(output)

if __name__ == "__main__":
    run()
