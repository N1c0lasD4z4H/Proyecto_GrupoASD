from fastapi import APIRouter, HTTPException, BackgroundTasks
from Services.issue_service import GithubIssueService
from Models.issue_analysis import IssueTimeStats
from Elastic.index_dispatcher import send_document
import logging

router = APIRouter(prefix="/issues", tags=["issues"])
logger = logging.getLogger(__name__)

@router.get("/{owner}/{repo}/issuesanalysis", summary="Analyze issues in a repository")
async def get_issues_analysis(owner: str, repo: str, background_tasks: BackgroundTasks):
    try:
        analysis = GithubIssueService.analyze_issues(owner, repo)

        if "error" in analysis:
            raise HTTPException(status_code=400, detail=analysis["error"])

        # Validar con el modelo Pydantic
        document = IssueTimeStats(**analysis)

        # Enviar a Elasticsearch en segundo plano
        background_tasks.add_task(send_document, "github_issues_analysis", document.repository, document)

        return document

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error processing issues for {owner}/{repo}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
