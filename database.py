from sqlmodel import SQLModel, create_engine

sqlite_file_name = "medication_app.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

def create_db_and_tables():
    """Creates the tables if they don't exist yet."""
    SQLModel.metadata.create_all(engine)
