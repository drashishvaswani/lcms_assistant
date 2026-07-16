from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

from app.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String, nullable=False)

    upload_date = Column(DateTime, default=datetime.utcnow)

    text = Column(Text)