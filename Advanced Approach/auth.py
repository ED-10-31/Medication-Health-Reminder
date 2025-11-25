from sqlmodel import select
from database import get_session, User


def register_user(username, password):
    """
    Creates a new user.
    Returns: True if successful, False if username already exists.
    """
    session = get_session()

    statement = select(User).where(User.username == username)
    existing_user = session.exec(statement).first()

    if existing_user:
        session.close()
        return False

    new_user = User(username=username, password=password)
    session.add(new_user)
    session.commit()
    session.close()
    return True


def login_user(username, password):
    """
    Checks credentials.
    Returns: The user_id (int) if successful, or None if failed.
    """
    session = get_session()

    statement = select(User).where(User.username == username)
    user = session.exec(statement).first()
    session.close()

    if user and user.password == password:
        return user.id

    return None
