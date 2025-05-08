from pydantic import BaseModel
from typing import List, Optional


class UserRepository(BaseModel):
    name: str
    url: str
    created_at: str
    updated_at: str
    language: Optional[str]
    open_issues: int
    size: int
    is_fork: bool


class RepoMetadata(BaseModel):
    total_repos: int               
    timestamp: str


class UserRepoDocument(BaseModel):
    username: str
    repositories: List[UserRepository]
    metadata: RepoMetadata         