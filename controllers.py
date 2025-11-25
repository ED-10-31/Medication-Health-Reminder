from sqlmodel import Session, select
from database import engine
from models import Medication, HistoryLog
from datetime import datetime

def calculate_daily_consumption(frequency: str) -> int:
    mapping = {
        "Once a day": 1,
        "Twice a day": 2,
        "Thrice a day": 3,
        "Once every two days": 0
    }
    return mapping.get(frequency, 1)

def add_medication(name, dosage, total_pills, frequency, scheduled_time):
    """Adds a new medication to the database."""
    daily_use = calculate_daily_consumption(frequency)
    
    new_med = Medication(
        name=name,
        dosage=dosage,
        total_pills=total_pills,
        frequency=frequency,
        scheduled_time=scheduled_time,
        daily_consumption=daily_use
    )
    
    with Session(engine) as session:
        session.add(new_med)
        session.commit()
        session.refresh(new_med)
        return f"Success: {new_med.name} added."

def mark_taken(med_id: int):
    """Decrements stock and logs history."""
    with Session(engine) as session:
        med = session.get(Medication, med_id)
        if not med:
            return "Error: Medication not found."
        
        if med.total_pills > 0:
            med.total_pills -= 1
            session.add(med)
        
        log = HistoryLog(
            med_id=med.id, 
            med_name=med.name, 
            status="Taken"
        )
        session.add(log)
        
        session.commit()
        
        if med.daily_consumption > 0:
            days_left = med.total_pills / med.daily_consumption
            if days_left <= 3:
                return f"Taken. WARNING: Only {int(days_left)} days supply left!"
        
        return "Medication marked as taken."

def get_all_meds():
    with Session(engine) as session:
        statement = select(Medication)
        return session.exec(statement).all()
