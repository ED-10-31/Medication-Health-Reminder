from database import create_db_and_tables
from alarm_service import AlarmService
import controllers

create_db_and_tables()

alarm = AlarmService()
alarm.start()

def main_menu():
    print("\n--- MEDICATION APP (No Audio) ---")
    print("1. Add Medication")
    print("2. List Medications")
    print("3. Take Medication")
    print("4. Exit")

    while True:
        choice = input("\nSelect Option: ")
        
        if choice == "1":
            name = input("Name: ")
            dosage = input("Dosage: ")
            pills = int(input("Total Pills: "))
            freq = "Once a day"
            time_sched = input("Schedule Time (HH:MM, 24hr): ")
            
            msg = controllers.add_medication(name, dosage, pills, freq, time_sched)
            print(msg)
            
        elif choice == "2":
            meds = controllers.get_all_meds()
            for m in meds:
                print(f"[{m.id}] {m.name} - {m.scheduled_time}")
                
        elif choice == "3":
            med_id = int(input("Enter ID: "))
            msg = controllers.mark_taken(med_id)
            print(msg)
            
        elif choice == "4":
            print("Stopping...")
            alarm.stop()
            break

if __name__ == "__main__":
    main_menu()
