from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class ImportLogResponse(BaseModel):
    id: int
    filename: str
    total_rows: int
    successful_rows: int
    failed_rows: int
    errors: Optional[str] = None
    status: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ImportLogListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    items: List[ImportLogResponse]


class ImportResult(BaseModel):
    log_id: int
    filename: str
    total_rows: int
    successful_rows: int
    failed_rows: int
    status: str
    message: str
    errors: Optional[List[dict]] = None
