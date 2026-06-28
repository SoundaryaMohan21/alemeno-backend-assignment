from pydantic import BaseModel
from datetime import datetime


class JobResponse(BaseModel):
    id: int
    filename: str
    status: str
    row_count_raw: int
    row_count_clean: int
    created_at: datetime

    class Config:
        from_attributes = True