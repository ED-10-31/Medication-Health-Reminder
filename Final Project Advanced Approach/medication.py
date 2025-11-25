from sqlmodel import select
from datetime import datetime
from database import get_session, Medication, History


def add_medication(user_id: int, name: str, total_pills: int, pills_per_day: int):
    session = get_session()
    new_med = Medication(
        user_id=user_id,
        name=name,
        total_pills=total_pills,
        pills_per_day=pills_per_day
    )
    session.add(new_med)
    session.commit()
    session.refresh(new_med)
    session.close()
    return True


def get_user_medications(user_id: int):
    """
    Fetches meds and calculates Smart Refill stats.
    """
    session = get_session()
    statement = select(Medication).where(Medication.user_id == user_id)
    results = session.exec(statement).all()

    output_list = []

    for med in results:
        if med.pills_per_day > 0:
            days_remaining = int(med.total_pills / med.pills_per_day)
        else:
            days_remaining = 999

        is_low_stock = days_remaining < 3

        med_dict = med.model_dump()
        med_dict["days_remaining"] = days_remaining
        med_dict["alert"] = is_low_stock

        output_list.append(med_dict)

    session.close()
    return output_list



def take_medication(med_id: int, amount: int = 1):
    session = get_session()

    med = session.get(Medication, med_id)

    if not med:
        session.close()
        return False, 0

    med.total_pills = max(0, med.total_pills - amount)
    session.add(med)

    log = History(med_id=med_id, taken_at=datetime.now())
    session.add(log)

    session.commit()

    new_stock = med.total_pills
    session.close()

    return True, new_stock


def get_medication_history(user_id: int):
    session = get_session()

    statement = select(Medication.name, History.taken_at).join(History).where(Medication.user_id == user_id).order_by(
        History.taken_at.desc())

    results = session.exec(statement).all()
    session.close()

    history_list = []
    for name, taken_at in results:
        history_list.append({
            "medication_name": name,
            "time_taken": taken_at.strftime("%Y-%m-%d %H:%M:%S")
        })

    return history_list
