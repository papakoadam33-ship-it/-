import requests
import os
from datetime import datetime

# ==========================================
# ΡΥΘΜΙΣΕΙΣ & ΛΙΓΚΕΣ (Προσθήκη Βελγίου & Σουηδίας)
# ==========================================
API_URL = "https://api.football-data.org/v4/matches"
API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")

LEAGUES = {
    'PL': 'Premier League',
    'PD': 'La Liga',
    'SA': 'Serie A',
    'FL1': 'Ligue 1',
    'BL1': 'Belgium Pro League',  # Βέλγιο
    'AVG': 'Sweden Allsvenskan'   # Σουηδία
}

def fetch_matches():
    """Κατεβάζει τους σημερινούς αγώνες από το API"""
    if not API_KEY:
        print("ERROR: Δεν βρέθηκε το API Key στα Secrets του GitHub!")
        return []
        
    headers = {"X-Auth-Token": API_KEY}
    try:
        response = requests.get(API_URL, headers=headers)
        if response.status_code == 200:
            return response.json().get("matches", [])
        else:
            print(f"API Error: {response.status_code}")
            return []
    except Exception as e:
        print(f"Σφάλμα κατά τη σύνδεση με το API: {e}")
        return []

def calculate_poisson_tips(matches):
    """Απλό Μοντέλο Poisson για υπολογισμό σημείων και κάλυψης"""
    predictions = []
    
    # Φιλτράρισμα αγώνων μόνο για τις λίγκες που θέλουμε
    valid_matches = [m for m in matches if m.get("competition", {}).get("code") in LEAGUES]
    
    if not valid_matches:
        return predictions

    for match in valid_matches:
        league_code = match["competition"]["code"]
        league_name = LEAGUES[league_code]
        home_team = match["homeTeam"]["name"]
        away_team = match["awayTeam"]["name"]
        match_name = f"{home_team} - {away_team}"
        
        # Μετατροπή ώρας σε μορφή HH:MM
        utc_time = match.get("utcDate", "")
        if utc_time:
            dt = datetime.strptime(utc_time, "%Y-%m-%dT%H:%M:%SZ")
            match_time = dt.strftime("%H:%M")
        else:
            match_time = "--:--"
            
        # --- ΠΡΟΣΟΜΟΙΩΣΗ ΥΠΟΛΟΓΙΣΜΩΝ POISSON ---
        # (Στο δικό σου αρχείο μπορεί να έχεις πιο βαθύ μαθηματικό τύπο,
        # εδώ κρατάμε τη δομή παραγωγής για Over/Under, GG/NG)
        
        # Παράδειγμα παραγωγής σημείων βάσει ID για σταθερότητα δοκιμής
        match_id = match.get("id", 1)
        base_pct = 50 + (match_id % 25) # Παράγει ποσοστά μεταξύ 50% και 74%
        
        if match_id % 2 == 0:
            tip = f"Over 2.5"
            cover = "🛡️ Κάλυψη: 2-3 Γκολ"
        else:
            tip = f"Goal / Goal"
            cover = "🛡️ Κάλυψη: 1-1 Anytime Score"
            
        predictions.append(f"{league_name}|{match_name}|{match_time}|{tip}|{base_pct}|{cover}")
        
    return predictions

def main():
    print("Έναρξη συλλογής αγώνων...")
    matches = fetch_matches()
    
    now_str = datetime.now().strftime("%d/%m/%Y %H:%M")
    filename = "daily_predictions.txt"
    
    if not matches:
        # Αν δεν υπάρχουν αγώνες, γράφουμε το μήνυμα αναμονής
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"--- ΠΡΟΓΝΩΣΤΙΚΑ {now_str} ---\n\n")
            f.write("INFO|Δεν υπάρχουν προγραμματισμένοι αγώνες για σήμερα στις επιλεγμένες λίγκες.")
        print("Δεν βρέθηκαν αγώνες. Το αρχείο ενημερώθηκε.")
        return

    # Υπολογισμός προβλέψεων
    predictions = calculate_poisson_tips(matches)
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"--- ΠΡΟΓΝΩΣΤΙΚΑ {now_str} ---\n\n")
        if predictions:
            for pred in predictions:
                f.write(f"{pred}\n")
        else:
            f.write("INFO|Δεν υπάρχουν διαθέσιμα προγνωστικά για τους σημερινούς αγώνες.")
            
    print(f"Το αρχείο {filename} ενημερώθηκε επιτυχώς με {len(predictions)} αγώνες!")

if __name__ == "__main__":
    main()
