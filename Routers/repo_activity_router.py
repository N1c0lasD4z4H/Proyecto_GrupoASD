from datetime import datetime, timedelta
from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException, BackgroundTasks
from Services.repo_activity_service import GitHubService
from Models.repo_activity import RepoActivityDocument
from Elastic.index_dispatcher import send_document
import logging

router = APIRouter()
github_service = GitHubService()
logger = logging.getLogger(__name__)

@router.get("/{owner}/{repo}/activity", summary="Get repository activity")
async def get_repo_activity(owner: str, repo: str, background_tasks: BackgroundTasks):
    try:
        # Validación de parámetros
        if not owner or not repo:
            raise HTTPException(status_code=400, detail="Owner and repository name are required")

        # Obtener datos del servicio
        activity_data = await github_service.get_repo_activity(owner, repo)

        # Manejar errores del servicio
        if activity_data.get("status") == "error":
            error_msg = activity_data.get("error", "Unknown error")
            if "not found" in error_msg.lower():
                raise HTTPException(status_code=404, detail="Repository not found")
            elif "invalid" in error_msg.lower() or "token" in error_msg.lower():
                raise HTTPException(status_code=401, detail="Invalid GitHub token")
            else:
                raise HTTPException(status_code=500, detail=error_msg)

        # Asegurar campos requeridos
        activity_data.setdefault("commit_history", [])
        activity_data.setdefault("weekly_activity", {
            "period_start": (datetime.utcnow() - timedelta(days=7)).isoformat(),
            "period_end": datetime.utcnow().isoformat(),
            "count_by_author": {},
            "total": 0
        })
        activity_data.setdefault("authors", [])

        # Crear documento validado
        document = RepoActivityDocument(
            repo_id=f"{owner}_{repo}",
            owner=owner,
            repo=repo,
            total_commits=activity_data.get("total_commits", 0),
            last_commit=activity_data.get("last_commit"),
            weekly_activity=activity_data["weekly_activity"],
            commit_history=activity_data["commit_history"],
            authors=activity_data["authors"],
            processed_at=datetime.utcnow().isoformat()
        )

        # Enviar a Elasticsearch en segundo plano
        background_tasks.add_task(send_document, "github_repo_activity", document.repo_id, document)

        # Respuesta simplificada para el cliente
        return {
            "repo": repo,
            "owner": owner,
            "total_commits": document.total_commits,
            "last_commit": document.last_commit,
            "weekly_activity": document.weekly_activity,
            "authors": document.authors
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
