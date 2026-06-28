from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    DateTime,
    ForeignKey
)

from app.core.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    # Link every transaction to a processing job
    job_id = Column(
        Integer,
        ForeignKey("jobs.id"),
        nullable=False
    )

    txn_id = Column(
        String,
        unique=True,
        nullable=False
    )

    date = Column(DateTime)

    merchant = Column(String)

    amount = Column(Float)

    currency = Column(String)

    status = Column(String)

    category = Column(String)

    account_id = Column(String)

    notes = Column(String)

    anomaly = Column(
        String,
        default="No"
    )