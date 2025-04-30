from fastapi import APIRouter, HTTPException, BackgroundTasks
from Services.template_service import FileCheckService
from Elastic.elastic_service import es  
from typing import Dict, Any
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

async def send_to_elastic(data: Dict[str, Any], index_name: str = "github_template"):
    """
    Envía datos a Elasticsearch.
    """
    try:
        if not data.get("user_or_org"):
            logger.error("Falta el campo 'user_or_org' en los datos")
            return

        await es.index(
            index=index_name,
            id=data["user_or_org"],
            document=data
        )
        logger.info(f"Datos indexados correctamente para {data['user_or_org']}")

    except Exception as e:
        logger.error(f"Error al indexar en Elasticsearch: {str(e)}")
        raise

@router.get("/users/{user_or_org}/check-pull-request-templates")
async def check_pull_request_templates(
    user_or_org: str, 
    background_tasks: BackgroundTasks
):
    """
    Endpoint para verificar templates de PR
    """
    try:
        result = FileCheckService.analyze_pull_request_template(user_or_org)
        
        if not result:
            raise HTTPException(
                status_code=404,
                detail="No se encontraron templates"
            )

        
        if "user_or_org" not in result:
            result["user_or_org"] = user_or_org

        #Enviar a Elastic en background
        background_tasks.add_task(send_to_elastic, result)
        
        return {
            "status": "success",
            "data": result,
            "message": "Resultados enviados para procesamiento"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en el endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno: {str(e)}"
        )