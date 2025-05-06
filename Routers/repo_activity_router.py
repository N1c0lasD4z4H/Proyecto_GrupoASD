from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, Any
from Services.repo_activity_service import GitHubService
from Elastic.elastic_service import es  
from datetime import datetime
import httpx
import logging

router = APIRouter()
github_service = GitHubService()
logger = logging.getLogger(__name__)

async def send_to_elastic(data: Dict[str, Any], index_name: str = "github_repo_activity"):
    """
    Envía datos a Elasticsearch en segundo plano con manejo de errores mejorado.
    """
    try:
        if not data.get("repo") or not data.get("owner"):
            logger.error("Missing required fields for Elasticsearch indexing")
            return

        doc_id = f"{data['owner']}_{data['repo']}"
        
        await es.index(
            index=index_name,
            id=doc_id,
            document=data
        )
        logger.info(f"Successfully indexed data for {doc_id}")
    except Exception as e:
        logger.error(f"Error indexing to Elasticsearch: {str(e)}")
        raise

@router.get("/{owner}/{repo}/activity", 
           summary="Get repository activity",
           response_description="Repository commit activity data",
           responses={
               200: {"description": "Successfully retrieved activity data"},
               401: {"description": "Invalid or missing GitHub token"},
               404: {"description": "Repository not found"},
               500: {"description": "Internal server error"}
           })
async def get_repo_activity(
    owner: str,
    repo: str,
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """
    Get commit activity data for a GitHub repository including:
    - Total commits
    - Weekly activity by author
    - Last commit date
    - Detailed commit history
    """
    try:
        # Validación básica de parámetros
        if not owner or not repo:
            raise HTTPException(
                status_code=400,
                detail="Owner and repository name are required"
            )

        # Obtener datos del servicio (sin token explícito)
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

        # Preparar datos para Elasticsearch
        elastic_data = activity_data.copy()
        elastic_data["repo_id"] = f"{owner}_{repo}"
        elastic_data["processed_at"] = datetime.utcnow().isoformat()

        # Enviar a Elasticsearch en background
        background_tasks.add_task(send_to_elastic, elastic_data)
        
        # Simplificar respuesta para el cliente
        response_data = {
            "repo": repo,
            "owner": owner,
            "total_commits": activity_data.get("total_commits", 0),
            "last_commit": activity_data.get("last_commit"),
            "weekly_activity": activity_data.get("weekly_activity", {}),
            "authors": activity_data.get("authors", [])
        }
        
        return response_data

    except httpx.HTTPStatusError as e:
        logger.error(f"GitHub API error: {str(e)}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"GitHub API error: {e.response.text}"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
