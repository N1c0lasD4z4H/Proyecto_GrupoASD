from pydantic import BaseModel, field_validator
from typing import List, Optional, Dict, Any
from datetime import datetime

class IssueTimeItem(BaseModel):
    # ... (campos existentes)    issue_id: int
    number: int
    url: str
    author: Optional[str]
    title: str
    labels: List[str]
    created_at: str
    closed_at: Optional[str]
    state: str  # open, closed
    resolution_time: Optional[float]  # seconds
    last_response_time: float  # seconds 
    @field_validator("created_at", "closed_at")
    def validate_dates(cls, value):
        if value:
            try:
                datetime.fromisoformat(value.replace("Z", "+00:00"))
                return value
            except ValueError:
                raise ValueError("Formato de fecha inválido")
        return value





class IssueTimeStatsSummary(BaseModel):
    total: int
    open: int
    closed: int
    avg_resolution_time: Optional[float]  # in days


class IssueTimeStats(BaseModel):
    repository: str
    stats: IssueTimeStatsSummary
    issues: List[IssueTimeItem]
    timestamp: str
    def model_dump(self, **kwargs):
        return super().model_dump(**kwargs)