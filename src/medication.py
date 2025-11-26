from datetime import datetime
from database import DATA_STORE, save_data, get_next_id

def add_medication(user_id, name, total_pills, pills_per_day):
    new_id = get_next_id("medications")

    med_dict = {
        "id": new_id,
        "user_id": user_id,
        "name": name,
        "total_pills": total_pills,
        "pills_per_day": pills_per_day
    }

    DATA_STORE["medications"].append(med_dict)
    save_data()
    return True


def get_user_medications(user_id):
    """
    Returns a list of meds for the user with calculated Days Remaining.
    """
    output_list = []

    for med in DATA_STORE["medications"]:
        if med["user_id"] == user_id:

            current_stock = med["total_pills"]
            daily_dose = med["pills_per_day"]

            if daily_dose > 0:
                days_remaining = int(current_stock / daily_dose)
            else:
                days_remaining = 999

            is_low_stock = days_remaining < 3

            med_for_ui = med.copy()
            med_for_ui["days_remaining"] = days_remaining
            med_for_ui["alert"] = is_low_stock

            output_list.append(med_for_ui)

    return output_list


def take_medication(med_id, amount=1):
    found_med = None
    for med in DATA_STORE["medications"]:
        if med["id"] == med_id:
            found_med = med
            break

    if not found_med:
        return False, 0

    current = found_med["total_pills"]
    new_stock = max(0, current - amount)
    found_med["total_pills"] = new_stock

    history_entry = {
        "med_id": med_id,
        "medication_name": found_med["name"],
        "taken_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    DATA_STORE["history"].append(history_entry)

    save_data()
    return True, new_stock


def get_medication_history(user_id):
    """
    Filters history logs.
    """
    user_med_ids = []
    for med in DATA_STORE["medications"]:
        if med["user_id"] == user_id:
            user_med_ids.append(med["id"])

    user_history = [log for log in DATA_STORE["history"] if log["med_id"] in user_med_ids]

    user_history.sort(key=lambda x: x["taken_at"], reverse=True)

    result = []
    for log in user_history:
        result.append({
            "medication_name": log["medication_name"],
            "time_taken": log["taken_at"]
        })

    return result
