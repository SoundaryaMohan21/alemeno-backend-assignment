from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.core.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String)

    file_path = Column(String)

    status = Column(String, default="PENDING")

    row_count_raw = Column(Integer, default=0)

    row_count_clean = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)

    completed_at = Column(DateTime, nullable=True)

    error_message = Column(String, nullable=True)