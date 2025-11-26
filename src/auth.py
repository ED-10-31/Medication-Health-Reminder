from database import DATA_STORE, save_data, get_next_id


def register_user(username, password):
    """
    Registers a new user into the list.
    """
    for user in DATA_STORE["users"]:
        if user["username"] == username:
            return False

    new_id = get_next_id("users")
    new_user = {
        "id": new_id,
        "username": username,
        "password": password
    }

    DATA_STORE["users"].append(new_user)
    save_data()
    return True


def login_user(username, password):
    """
    Loops through users to find a match.
    Returns user_id or None.
    """
    for user in DATA_STORE["users"]:
        if user["username"] == username and user["password"] == password:
            return user["id"]

    return None
