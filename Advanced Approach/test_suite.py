import os
from database import init_db
from auth import register_user, login_user
from medication import add_medication, get_user_medications, take_medication, get_medication_history
from exporter import generate_pdf_report


def main():
    print("=================================================")
    print("      MEDICATION APP - BACKEND TEST SUITE        ")
    print("=================================================")

    # --- STEP 1: INITIALIZATION ---
    print("\n[Step 1] Initializing Database...")
    if os.path.exists("medication_app.db"):
        os.remove("medication_app.db")  # Clean slate for testing
        print("  -> Old database removed.")

    init_db()
    print("  -> Database initialized successfully.")

    # --- STEP 2: AUTHENTICATION ---
    print("\n[Step 2] Testing Authentication...")
    username = "grandma_test"
    password = "secure_password_123"

    # Register
    if register_user(username, password):
        print(f"  -> Registration successful for '{username}'.")
    else:
        print(f"  -> User '{username}' already exists.")

    # Login
    user_id = login_user(username, password)
    if user_id:
        print(f"  -> Login successful! User ID is: {user_id}")
    else:
        print("  -> Login Failed.")
        return  # Stop test if login fails

    # --- STEP 3: ADDING MEDICATIONS ---
    print("\n[Step 3] Adding Medications...")

    # Med 1: Healthy stock (30 pills, 1 per day = 30 days left)
    add_medication(user_id, "Lisinopril (Heart)", 30, 1)
    print("  -> Added 'Lisinopril' (30 pills, 1/day).")

    # Med 2: LOW stock (4 pills, 2 per day = 2 days left -> ALERT!)
    add_medication(user_id, "Metformin (Diabetes)", 4, 2)
    print("  -> Added 'Metformin' (4 pills, 2/day).")

    # --- STEP 4: SMART REFILL LOGIC ---
    print("\n[Step 4] Testing Smart Refill & Alerts...")
    meds = get_user_medications(user_id)

    for med in meds:
        status = "OK"
        if med['alert']:
            status = "!!! LOW STOCK WARNING !!!"

        # FIX: Changed med['stock'] to med['total_pills'] to match the SQLModel definition
        print(
            f"  -> Med: {med['name']:<20} | Stock: {med['total_pills']} | Days Left: {med['days_remaining']} | Status: {status}")

    # --- STEP 5: TAKING MEDICATION ---
    print("\n[Step 5] Taking Medication...")

    # Let's take the first medication found
    target_med_id = meds[0]['id']
    med_name = meds[0]['name']

    print(f"  -> User takes 1 pill of {med_name}...")
    success, new_stock = take_medication(target_med_id, 1)

    if success:
        print(f"  -> Success! New Stock for {med_name}: {new_stock}")
    else:
        print("  -> Error taking medication.")

    # --- STEP 6: VERIFYING HISTORY ---
    print("\n[Step 6] Verifying History Log...")
    history = get_medication_history(user_id)
    for log in history:
        print(f"  -> Logged: Took {log['medication_name']} at {log['time_taken']}")

    # --- STEP 7: PDF EXPORT ---
    print("\n[Step 7] Testing PDF Export...")
    pdf_name = "test_report.pdf"
    if generate_pdf_report(user_id, pdf_name):
        print(f"  -> PDF generated successfully: {pdf_name}")
        print("  -> Please check your folder to view the file.")
    else:
        print("  -> PDF generation failed.")

    print("\n=================================================")
    print("              TEST SUITE COMPLETED               ")
    print("=================================================")


if __name__ == "__main__":
    main()
