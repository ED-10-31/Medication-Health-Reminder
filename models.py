from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime

class Medication(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    dosage: str
    total_pills: int
    frequency: str 
    scheduled_time: str
    daily_consumption: int
    last_alert_date: Optional[str] = None

class HistoryLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    med_id: int
    med_name: str
    status: str             # "Taken", "Missed"
    timestamp: datetime = Field(default_factory=datetime.now)