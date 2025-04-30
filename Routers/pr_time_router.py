# routers/template_router.py
from fastapi import APIRouter, HTTPException, BackgroundTasks
from Services.pr_time_service import PRDashboardService
from Elastic.elastic_service import es

router = APIRouter()

async def send_to_elastic(data: dict, index_name: str = "github_pr_time"):
    """
    Envía datos a Elasticsearch.
    """
    try:
        # Usar la clave 'owner_repo' como ID del documento en Elasticsearch
        await es.index(
            index=index_name,
            id=data["owner_repo"],  
            document=data
        )
    except Exception as e:
        raise RuntimeError(f"Error al indexar en Elasticsearch: {str(e)}")


@router.get("/prs/{owner}/{repo}")
def get_dashboard_prs(owner: str, repo: str, background_tasks: BackgroundTasks):
    try:
        data = PRDashboardService.get_enriched_pull_requests(owner, repo)
        
        # Enviar datos en segundo plano a Elasticsearch
        background_tasks.add_task(send_to_elastic, data)
        
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
