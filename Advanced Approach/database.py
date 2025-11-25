from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, create_engine, Session, select

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    password: str

class Medication(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    name: str
    total_pills: int
    pills_per_day: int

class History(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    med_id: int = Field(foreign_key="medication.id")
    taken_at: datetime


sqlite_file_name = "medication_app.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url)

def init_db():
    """Creates the database and tables automatically"""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Returns a database session"""
    return Session(engine)
