from fastapi import APIRouter, HTTPException, BackgroundTasks
from Services.template_service import FileCheckService
from Elastic.elastic_service import es
from datetime import datetime
from typing import Dict, Any
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

async def send_to_elastic(data: Dict[str, Any], index_name: str = "github_template"):
    """Envía datos a Elasticsearch con mejor manejo de errores"""
    try:
        if not data.get("user_or_org"):
            logger.error("Missing user_or_org field")
            return

        doc_id = f"{data['user_or_org']}_{datetime.utcnow().timestamp()}"
        
        await es.index(
            index=index_name,
            id=doc_id,
            document=data
        )
        logger.info(f"Data indexed for {data['user_or_org']}")
    except Exception as e:
        logger.error(f"Elasticsearch error: {str(e)}")
        raise

@router.get("/users/{user_or_org}/check-pull-request-templates")
async def check_pull_request_templates(
    user_or_org: str, 
    background_tasks: BackgroundTasks
):
    """Endpoint mejorado con validación y logging"""
    try:
        if not user_or_org:
            raise HTTPException(status_code=400, detail="User/org name is required")

        result = await FileCheckService.analyze_pull_request_template(user_or_org)
        
        if "error" in result:
            raise HTTPException(
                status_code=400,
                detail=result["error"]
            )

        if not result.get("repositories"):
            raise HTTPException(
                status_code=404,
                detail="No repositories found to analyze"
            )

        # Enviar a Elastic en background
        background_tasks.add_task(send_to_elastic, result)
        
        return {
            "status": "success",
            "user": user_or_org,
            "stats": result.get("stats"),
            "sample_data": result["repositories"][:5]  # Mostrar solo muestra
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )