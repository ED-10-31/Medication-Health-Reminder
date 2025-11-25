import json
import os

DB_FILE = "med_data.json"

DATA_STORE = {
    "users": [],
    "medications": [],
    "history": []
}


def init_db():
    """
    Checks if the JSON file exists. If not, creates it.
    If it does, loads the data into our DATA_STORE variable.
    """
    global DATA_STORE
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            DATA_STORE = json.load(f)
    else:
        save_data()


def save_data():
    """Writes the current DATA_STORE to the JSON file."""
    with open(DB_FILE, "w") as f:
        json.dump(DATA_STORE, f, indent=4)


def get_next_id(table_key):
    """
    Helper function to simulate Auto-Increment ID.
    Finds the highest ID in the list and adds 1.
    """
    current_list = DATA_STORE.get(table_key, [])
    if not current_list:
        return 1

    existing_ids = [item["id"] for item in current_list]
    return max(existing_ids) + 1
