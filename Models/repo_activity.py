from pydantic import BaseModel
from typing import List, Dict, Optional


class CommitEntry(BaseModel):
    author: str
    date: str  # ISO string
    message: str
    sha: str


class WeeklyActivity(BaseModel):
    period_start: str
    period_end: str
    count_by_author: Dict[str, int]
    total: int


class RepoActivityDocument(BaseModel):
    repo_id: str
    owner: str
    repo: str
    total_commits: int
    last_commit: Optional[str]
    weekly_activity: WeeklyActivity
    commit_history: List[CommitEntry]
    authors: List[str]
    processed_at: str
