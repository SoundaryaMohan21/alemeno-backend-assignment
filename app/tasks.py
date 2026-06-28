from datetime import datetime
import pandas as pd

from app.worker import celery_app
from app.core.database import SessionLocal
from app.models.job import Job

from app.services.csv_processor import read_csv
from app.services.transaction_service import save_transactions
from app.services.llm_service import (
    classify_transactions,
    generate_summary,
)


@celery_app.task(
    name="app.tasks.process_csv",
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def process_csv(job_id: int, file_path: str):

    db = SessionLocal()

    try:

        job = db.query(Job).filter(Job.id == job_id).first()

        if job is None:
            return

        # ----------------------------
        # Read CSV
        # ----------------------------
        df = read_csv(file_path)

        job.row_count_raw = len(df)

        # ----------------------------
        # Clean Amount Column
        # ----------------------------
        df["amount"] = (
            df["amount"]
            .astype(str)
            .str.replace("$", "", regex=False)
            .str.replace(",", "", regex=False)
            .str.strip()
        )

        df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
        df["amount"] = df["amount"].fillna(0)

        # ----------------------------
        # LLM Category Classification
        # ----------------------------
        missing = df[
            df["category"].isna()
            | (df["category"].astype(str).str.strip() == "")
        ]

        if len(missing):

            payload = []

            for _, row in missing.iterrows():

                payload.append({
                    "merchant": row["merchant"],
                    "notes": str(row["notes"]),
                    "amount": float(row["amount"]),
                })

            categories = classify_transactions(payload)

            if categories:
                df.loc[missing.index, "category"] = categories

        # ----------------------------
        # Save Transactions
        # ----------------------------
        saved_rows = save_transactions(df, db, job_id)

        job.row_count_clean = saved_rows

        # ----------------------------
        # LLM Spending Summary
        # ----------------------------
        summary = generate_summary({
            "total_transactions": saved_rows,
            "total_spend": float(df["amount"].sum()),
            "top_merchants": (
                df["merchant"]
                .value_counts()
                .head(5)
                .to_dict()
            ),
        })

        print("\n========== LLM SUMMARY ==========")
        print(summary)
        print("================================\n")

        job.status = "completed"
        job.completed_at = datetime.utcnow()

        db.commit()

        print(f"Job {job_id} completed.")

    except Exception as e:

        job = db.query(Job).filter(Job.id == job_id).first()

        if job:
            job.status = "failed"
            job.error_message = str(e)
            db.commit()

        raise

    finally:
        db.close()