from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class AuthorInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    email: str

class UserDailyCommitDocument(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    owner: str
    repo: str
    author: AuthorInfo
    date: str  # yyyy-MM-dd
    commit_count: int
    timestamp: datetime