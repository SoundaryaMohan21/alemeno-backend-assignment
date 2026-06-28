from sqlalchemy.orm import Session
from app.models.transaction import Transaction
from app.services.llm_service import detect_anomaly
import pandas as pd


def save_transactions(df, db: Session, job_id: int):

    df = df.drop_duplicates(subset=["txn_id"])

    saved = 0

    for _, row in df.iterrows():

        txn_id = str(row["txn_id"]).strip()

        # Skip if txn already exists in DB
        existing = (
            db.query(Transaction)
            .filter(Transaction.txn_id == txn_id)
            .first()
        )

        if existing:
            continue

        amount = (
            str(row["amount"])
            .replace("$", "")
            .replace(",", "")
            .strip()
        )

        transaction = Transaction(
            job_id=job_id,
            txn_id=txn_id,
            date=pd.to_datetime(row["date"]),
            merchant=str(row["merchant"]).strip(),
            amount=float(amount),
            currency=str(row["currency"]).upper().strip(),
            status=str(row["status"]).upper().strip(),
            category=(
                "Uncategorised"
                if pd.isna(row["category"]) or str(row["category"]).strip() == ""
                else str(row["category"]).strip()
            ),
            account_id=str(row["account_id"]).strip(),
            notes=""
            if pd.isna(row["notes"])
            else str(row["notes"]).strip(),
            anomaly=detect_anomaly(
                {
                    "merchant": row["merchant"],
                    "amount": amount,
                    "status": row["status"],
                    "category": row["category"],
                    "currency": row["currency"],
                }
            ),
        )

        db.add(transaction)
        saved += 1

    db.commit()

    return saved