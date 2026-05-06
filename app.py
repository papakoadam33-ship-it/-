if os.path.exists("daily_predictions.txt"):
    with open("daily_predictions.txt", "r", encoding="utf-8") as f:
        content = f.read()
        if content.strip():
            st.write(content) # Αυτό θα εμφανίσει το κείμενο απλά
        else:
            st.warning("Το αρχείο είναι άδειο. Περίμενε το API.")
else:
    st.error("Το αρχείο daily_predictions.txt δεν βρέθηκε!")

