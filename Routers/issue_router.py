from fastapi import APIRouter, HTTPException, BackgroundTasks
from Services.issue_service import GithubIssueService
from Models.issue_analysis import IssueTimeStats
from Elastic.bulk_dispatcher import send_bulk_documents  
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/issues/{owner}/{repo}/issuesanalysis")
async def get_issues_analysis(owner: str, repo: str, background_tasks: BackgroundTasks):
    try:
        analysis = GithubIssueService.analyze_issues(owner, repo)

        if "error" in analysis:
            raise HTTPException(status_code=400, detail=analysis["error"])

        document = IssueTimeStats(**analysis)
        
        # Preparar documentos para Elasticsearch
        documents = []
        
        # 1. Documento de estadísticas generales
        stats_doc = {
            "repository": document.repository,
            "timestamp": document.timestamp,
            "type": "summary",
            "stats": document.stats.model_dump()
        }
        documents.append(stats_doc)
        
        # 2. Documentos individuales para cada issue
        for issue in document.issues:
            issue_doc = issue.model_dump()
            issue_doc.update({
                "repository": document.repository,
                "timestamp": document.timestamp,
                "type": "issue"
            })
            documents.append(issue_doc)

        # Envío en bloque
        background_tasks.add_task(send_bulk_documents, "github_issues_analysis", documents)
        
        return document

    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")