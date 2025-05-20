from pydantic import BaseModel, field_validator
from typing import List, Optional
from datetime import datetime

class PRTimeItem(BaseModel):
    pr_id: int
    number: int
    url: str
    author: str
    created_at: str
    closed_at: Optional[str] = None
    merged_at: Optional[str] = None
    state: str  # open, closed, merged
    draft: bool
    review_count: int
    first_review_at: Optional[str] = None

    @field_validator("created_at", "closed_at", "merged_at", "first_review_at")
    def validate_date_format(cls, value):
        if value is None:
            return value
        try:
            datetime.fromisoformat(value.replace("Z", "+00:00"))
            return value
        except ValueError:
            raise ValueError("Formato de fecha inválido")

class PRTimeStatsSummary(BaseModel):
    total: int
    open: int
    closed: int
    merged: int
    with_reviews: int
    drafts: int
    conflicts: int

class PRTimeStats(BaseModel):
    repository: str
    stats: PRTimeStatsSummary
    pull_requests: List[PRTimeItem]
    timestamp: str