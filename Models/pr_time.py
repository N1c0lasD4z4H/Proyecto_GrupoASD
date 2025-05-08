from pydantic import BaseModel
from typing import List, Optional


class PRTimeItem(BaseModel):
    pr_id: int
    number: int
    url: str
    author: str
    created_at: str
    closed_at: Optional[str]
    merged_at: Optional[str]
    state: str  # open, closed, merged
    draft: bool
    review_count: int
    first_review_at: Optional[str]


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
