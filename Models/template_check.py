from pydantic import BaseModel
from typing import List, Optional


class TemplateRepoResult(BaseModel):
    repository: str
    has_template: bool
    template_path: Optional[str] = None
    error: Optional[str] = None


class TemplateStats(BaseModel):
    total: int
    with_template: int
    without_template: int


class TemplateCheckResult(BaseModel):
    user_or_org: str
    repositories: List[TemplateRepoResult]
    stats: TemplateStats
    timestamp: str
    error: Optional[str] = None  
