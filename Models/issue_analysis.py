from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class IssueTimeItem(BaseModel):
    issue_id: int
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