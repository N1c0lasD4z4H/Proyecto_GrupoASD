from pydantic import BaseModel
from typing import List, Dict, Optional


class PullRequestItem(BaseModel):
    id: int
    number: int
    title: str
    url: str
    state: str
    labels: List[str]
    created_at: Optional[str]
    updated_at: Optional[str]
    merged_at: Optional[str]
    user: Optional[str]


class LabelPRSummary(BaseModel):
    id: int
    number: int
    title: str
    url: str


class LabelStateGroup(BaseModel):
    count: int
    prs: List[LabelPRSummary]


class LabelClassification(BaseModel):
    total: int
    aceptado: LabelStateGroup
    cambios_solicitados: Optional[LabelStateGroup] = None


class PullRequestStats(BaseModel):
    total_prs: int
    prs_with_labels: int
    prs_aceptados: int
    prs_cambios_solicitados: int
    label_usage: Dict[str, int]


class RepoMetadata(BaseModel):
    owner: str
    repo: str
    processed_at: str


class PRStats(BaseModel):
    repo_id: str
    labels_classification: Dict[str, LabelClassification]
    individual_prs: Optional[List[PullRequestItem]] = []  # ← ahora opcional
    stats: PullRequestStats
    repo_metadata: RepoMetadata
