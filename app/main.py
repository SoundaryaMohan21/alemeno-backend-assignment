from fastapi import FastAPI

from app.core.database import Base, engine
from app.models.job import Job
from app.models.transaction import Transaction
from app.routers import jobs

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Alemeno Backend Assignment",
    description="AI-Powered Transaction Processing Pipeline",
    version="1.0.0",
    debug=True
)

# Register router
app.include_router(jobs.router)


@app.get("/")
def home():
    return {
        "message": "Welcome to Alemeno Backend Assignment!"
    }