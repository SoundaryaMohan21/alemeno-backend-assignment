# Alemeno Backend Assignment

# AI-Powered Transaction Processing Pipeline

A production-ready backend service built using **FastAPI**, **Celery**, **Redis**, **PostgreSQL**, and **Google Gemini AI** for processing financial transaction CSV files asynchronously.

The application validates uploaded CSV files, removes duplicate transactions, classifies uncategorized transactions using AI, detects suspicious transactions, generates spending summaries, and stores all cleaned records in PostgreSQL while tracking every processing job.

---

# Features

* Upload transaction CSV files
* Background processing using Celery
* Redis task queue integration
* Automatic duplicate transaction removal
* PostgreSQL database storage
* AI-powered transaction category classification using Google Gemini
* AI-powered anomaly detection
* AI-generated spending summary
* Job status tracking
* Retrieve processed transaction results
* RESTful APIs
* Interactive Swagger Documentation
* Dockerized deployment
* Modular and scalable project architecture

---

# Tech Stack

* Python 3.13
* FastAPI
* SQLAlchemy
* PostgreSQL
* Redis
* Celery
* Docker
* Docker Compose
* Pandas
* Google Gemini API
* Pydantic
* Uvicorn

---

# System Architecture

> Replace the image path below with your uploaded architecture diagram.

```text
README.md
architecture.png
```

```md
![System Architecture](architecture.png)
```

---

# Project Structure

```text
alemeno-assignment/
│
├── app/
│   ├── core/
│   │   └── database.py
│   │
│   ├── models/
│   │   ├── job.py
│   │   └── transaction.py
│   │
│   ├── routers/
│   │   └── jobs.py
│   │
│   ├── schemas/
│   │
│   ├── services/
│   │   ├── csv_processor.py
│   │   ├── llm_service.py
│   │   └── transaction_service.py
│   │
│   ├── worker.py
│   ├── tasks.py
│   └── main.py
│
├── uploads/
├── reports/
├── tests/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── README.md
└── .env
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/alemeno-backend-assignment.git

cd alemeno-backend-assignment
```

---

## Create Virtual Environment

Windows

```bash
python -m venv venv

venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file.

```env
GEMINI_API_KEY=your_gemini_api_key

DATABASE_URL=postgresql://postgres:postgres@localhost:5432/alemeno_db

REDIS_URL=redis://localhost:6379/0
```

---

## Start Docker Services

```bash
docker compose up -d
```

This starts:

* PostgreSQL
* Redis

---

## Start FastAPI Server

```bash
uvicorn app.main:app --reload
```

---

## Start Celery Worker

```bash
celery -A app.worker.celery_app worker --loglevel=info
```

---

# Swagger Documentation

After starting the application:

```
http://127.0.0.1:8000/docs
```

---

# API Endpoints

## Upload CSV

```
POST /jobs/upload
```

Uploads a transaction CSV file and starts asynchronous processing.

---

## List Jobs

```
GET /jobs
```

Returns all processing jobs.

---

## Get Job Status

```
GET /jobs/{job_id}/status
```

Returns processing status for a specific job.

---

## Get Job Results

```
GET /jobs/{job_id}/results
```

Returns processed transactions for a specific job.

---

# AI Features

The project integrates **Google Gemini** to provide intelligent financial analysis.

### Transaction Category Classification

Automatically classifies transactions whose category is missing.

Example Categories

* Food
* Shopping
* Travel
* Transport
* Utilities
* Entertainment
* Cash Withdrawal
* Other

---

### Anomaly Detection

Each transaction is analyzed by Gemini to determine whether it appears suspicious.

Possible Output

```
Yes
```

or

```
No
```

---

### Spending Summary

Gemini generates a financial summary including

* Spending insights
* Overall spending behaviour
* Risk level

Example

```json
{
    "narrative": "Most expenses were related to shopping and food. Spending is balanced with no major anomalies.",
    "risk_level": "Low"
}
```

---

# Sample Workflow

1. Upload CSV
2. Celery receives background task
3. CSV is validated
4. Duplicate transactions are removed
5. Missing categories are classified using Gemini
6. Transactions are checked for anomalies
7. Data is stored in PostgreSQL
8. Spending summary is generated
9. Job status is updated
10. Results are available through the API

---

# Example Upload Response

```json
{
    "job_id": 662686,
    "status": "PENDING",
    "message": "CSV uploaded successfully. Processing started."
}
```

---

# Example Job Status

```json
{
    "job_id": 662686,
    "status": "completed",
    "row_count_raw": 95,
    "row_count_clean": 82
}
```

---

# Improvements Implemented

* Duplicate transaction removal
* Duplicate database protection
* Background task processing
* AI-powered category prediction
* AI-powered anomaly detection
* AI-generated spending summary
* Job tracking
* PostgreSQL integration
* Redis queue
* Docker support
* Modular architecture
* Swagger documentation
* Error handling
* Logging

---

# Future Enhancements

* JWT Authentication
* Role-Based Access Control
* Batch upload support
* Email notifications
* Dashboard analytics
* Export processed transactions
* Unit and integration testing
* CI/CD pipeline

---

# Author

**Soundarya M**

B.Tech Artificial Intelligence & Data Science

KCG College of Technology

GitHub:
https://github.com/SoundaryaMohan21
