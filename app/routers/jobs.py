from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
import random
import os
import shutil

from app.core.database import get_db
from app.models.job import Job
from app.models.transaction import Transaction
from app.tasks import process_csv

router = APIRouter(prefix="/jobs", tags=["Jobs"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are allowed."
        )

    job_id = random.randint(100000, 999999)

    file_path = os.path.join(
        UPLOAD_DIR,
        f"{job_id}_{file.filename}"
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    job = Job(
        id=job_id,
        filename=file.filename,
        file_path=file_path,
        status="PENDING"
    )

    db.add(job)
    db.commit()

    result = process_csv.delay(job_id, file_path)

    print("=" * 60)
    print("TASK SENT TO CELERY")
    print("Task ID:", result.id)
    print("=" * 60)

    return {
        "job_id": job_id,
        "status": "PENDING",
        "message": "CSV uploaded successfully. Processing started."
    }


@router.get("")
def get_all_jobs(
    status: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(Job)

    if status:
        query = query.filter(Job.status == status)

    jobs = query.order_by(Job.created_at.desc()).all()

    return [
        {
            "job_id": job.id,
            "filename": job.filename,
            "status": job.status,
            "row_count_raw": job.row_count_raw,
            "row_count_clean": job.row_count_clean,
            "created_at": job.created_at,
            "completed_at": job.completed_at
        }
        for job in jobs
    ]


@router.get("/{job_id}/status")
def get_job_status(
    job_id: int,
    db: Session = Depends(get_db)
):
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found."
        )

    return {
        "job_id": job.id,
        "filename": job.filename,
        "status": job.status,
        "row_count_raw": job.row_count_raw,
        "row_count_clean": job.row_count_clean,
        "created_at": job.created_at,
        "completed_at": job.completed_at
    }


@router.get("/{job_id}/results")
def get_job_results(
    job_id: int,
    db: Session = Depends(get_db)
):
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found."
        )

    transactions = (
        db.query(Transaction)
        .filter(Transaction.job_id == job_id)
        .all()
    )

    return {
        "job": {
            "job_id": job.id,
            "filename": job.filename,
            "status": job.status,
            "row_count_raw": job.row_count_raw,
            "row_count_clean": job.row_count_clean,
            "created_at": job.created_at,
            "completed_at": job.completed_at
        },
        "transactions": [
            {
                "txn_id": txn.txn_id,
                "date": txn.date,
                "merchant": txn.merchant,
                "amount": txn.amount,
                "currency": txn.currency,
                "status": txn.status,
                "category": txn.category,
                "account_id": txn.account_id,
                "notes": txn.notes,
                "anomaly": txn.anomaly
            }
            for txn in transactions
        ]
    }