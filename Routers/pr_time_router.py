from fastapi import APIRouter, HTTPException, BackgroundTasks
from Services.pr_time_service import PRDashboardService
from Models.pr_time import PRTimeStats
from Elastic.bulk_dispatcher import async_send_bulk_documents
import logging
from pydantic import ValidationError

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/prs/{owner}/{repo}")
async def get_dashboard_prs(owner: str, repo: str, background_tasks: BackgroundTasks):
    try:
        data = await PRDashboardService.get_enriched_pull_requests(owner, repo)
        if "error" in data:
            raise HTTPException(status_code=400, detail=data["error"])

        pr_time_stats = PRTimeStats(**data)

        # Prepara documentos para Elasticsearch
        documents = []
        for pr in pr_time_stats.pull_requests:
            documents.append({
                **pr.model_dump(),
                "repository": pr_time_stats.repository,
                "timestamp": pr_time_stats.timestamp
            })

        # Añade estadísticas como un documento separado
        documents.append({
            "repository": pr_time_stats.repository,
            "timestamp": pr_time_stats.timestamp,
            "stats": pr_time_stats.stats.model_dump()
        })

        # Debug: Imprime los documentos antes de enviar
        logger.info(f"Preparando para enviar {len(documents)} documentos a Elasticsearch")

        background_tasks.add_task(async_send_bulk_documents, "github_pr_time", documents)
        return pr_time_stats

    except ValidationError as e:
        logger.error(f"Error de validación: {e.errors()}")
        raise HTTPException(status_code=400, detail="Datos inválidos")
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error interno del servidor")
