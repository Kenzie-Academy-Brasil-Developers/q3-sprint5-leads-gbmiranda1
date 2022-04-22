from dataclasses import dataclass
from sqlalchemy import Column, DateTime, String, Integer
from datetime import datetime
from app.configs.database import db

@dataclass
class LeadsModel(db.Model):

    __tablename__ = "leads_table"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    creation_date = Column(DateTime, default=datetime.now())
    last_visit = Column(DateTime, default=datetime.now())
    visits = Column(Integer, default=1)