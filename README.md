# Alemeno Backend Assignment

## Transaction Processing Pipeline API

A FastAPI-based backend service for uploading, validating, cleaning, and storing financial transaction data.

The application processes CSV files containing transaction records, removes duplicate transaction IDs, stores cleaned records in PostgreSQL, and maintains processing job history.

---

## Features

* Upload transaction CSV files
* Validate uploaded files
* Remove duplicate transaction IDs
* Store cleaned transactions in PostgreSQL
* Track every processing job
* Retrieve processing history
* Check processing status of individual jobs
* Swagger API documentation
* Logging support
* Clean project architecture

---

## Tech Stack

* Python 3.13
* FastAPI
* SQLAlchemy
* PostgreSQL
* Docker
* Pydantic
* Pandas
* Uvicorn

---

## Project Structure

```
alemeno-assignment/
│
├── app/
│   ├── core/
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   ├── workers/
│   └── main.py
│
├── uploads/
├── reports/
├── tests/
├── .env
├── README.md
└── requirements.txt
```

---

## Installation

### Clone repository

```bash
git clone <repository_url>
cd alemeno-assignment
```

### Create virtual environment

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

Linux

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Start PostgreSQL & Redis

```bash
docker compose up -d
```

---

## Run the API

```bash
uvicorn app.main:app --reload
```

Swagger UI

```
http://127.0.0.1:8000/docs
```

---

## API Endpoints

### Upload Transaction CSV

```
POST /jobs/upload
```

Uploads a CSV file, removes duplicate transaction IDs, stores cleaned transactions, and creates a processing job.

---

### List Processing Jobs

```
GET /jobs
```

Returns all processing jobs.

---

### Get Job Status

```
GET /jobs/{job_id}/status
```

Returns detailed information about a processing job.

---

## Sample Upload Response

```json
{
    "job_id": 17,
    "status": "completed",
    "filename": "transactions.csv",
    "rows_received": 95,
    "rows_saved": 82,
    "duplicates_removed": 13,
    "processing_time_ms": 118
}
```

---

## Improvements Added

* Duplicate transaction removal
* Duplicate database protection
* Job statistics
* Processing time measurement
* Logging
* Better Swagger documentation
* Professional API descriptions
* Processing summary response

---

## Author

Soundarya M
