import time
import threading
from datetime import datetime
from sqlmodel import Session, select
from database import engine
from models import Medication

class AlarmService:
    def __init__(self):
        self.running = False

    def start(self):
        """Starts the background thread to check time."""
        if not self.running:
            self.running = True
            t = threading.Thread(target=self._loop, daemon=True)
            t.start()
            print("🕒 Alarm Service Started (Background)...")

    def _loop(self):
        """Infinite loop checking time every 60 seconds."""
        while self.running:
            now = datetime.now()
            current_time = now.strftime("%H:%M")
            today_date = now.strftime("%Y-%m-%d")

            self._check_alarms(current_time, today_date)
            
            time.sleep(60)

    def _check_alarms(self, time_str, date_str):
        with Session(engine) as session:
            statement = select(Medication).where(
                Medication.scheduled_time == time_str
            )
            meds = session.exec(statement).all()

            for med in meds:
                if med.last_alert_date != date_str:
                    self._trigger_visual_alert(med)
                    
                    med.last_alert_date = date_str
                    session.add(med)
                    session.commit()

    def _trigger_visual_alert(self, med):
        """
        This function is called when the time matches.
        Currently: Prints to console.
        Future: Will call your GUI Pop-Up function.
        """
        print("\n" + "="*30)
        print(f"🔔 ALARM: Time to take {med.name} ({med.dosage})")
        print("="*30 + "\n")

    def stop(self):
        self.running = False
