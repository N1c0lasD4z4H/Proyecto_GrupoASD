from pydantic import BaseModel
from typing import List, Optional


class CommitInfo(BaseModel):
    repo_name: str
    total_commits: int
    first_commit: Optional[str]  # ISO8601 string
    last_commit: Optional[str]   # ISO8601 string
    is_empty: bool
    unique_authors_count: int
    unique_authors: List[str]


class UserCommitDocument(BaseModel):
    user: str
    total_repos: int
    repos_with_commits: int
    total_commits: int  # Agregado explícitamente
    commits: List[CommitInfo]
