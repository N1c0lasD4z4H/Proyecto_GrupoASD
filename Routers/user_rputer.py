from fastapi import APIRouter, HTTPException, BackgroundTasks
from Services.user_service import GithubUserService
from Elastic.elastic_service import es  
from typing import Dict, Any, List
import logging
from datetime import datetime

router = APIRouter()
logger = logging.getLogger(__name__)

async def send_to_elastic(data: Dict[str, Any], index_name: str = "github_user_repos"):
    """
    Envía datos estructurados de repositorios a Elasticsearch.
    """
    try:
        if not data.get("username"):
            logger.error("Campo 'username' faltante en los datos")
            return

        response = await es.index(
            index=index_name,
            id=data["username"],
            document={
                "username": data["username"],
                "repositories": data["repositories"],
                "metadata": {
                    "total_repos": data["total_repos"],
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
        )
        logger.info(f"Datos indexados para {data['username']} en índice {index_name}")
        return response

    except Exception as e:
        logger.error(f"Error Elasticsearch para {data.get('username', 'unknown')}: {str(e)}")
        raise

@router.get("/users/{username}/repositories")
async def get_user_repositories(
    username: str, 
    background_tasks: BackgroundTasks
):
    """
    Obtiene repositorios de usuario, procesa la información y envía a Elasticsearch.
    """
    try:
        # 1. Obtener datos del servicio
        repositories = await GithubUserService.get_user_repos_info(username)
        
        if not repositories:
            raise HTTPException(
                status_code=404,
                detail=f"No se encontraron repositorios para el usuario {username}"
            )

        # 2. Estructurar datos para Elasticsearch
        elastic_data = {
            "username": username,
            "repositories": repositories,
            "total_repos": len(repositories)
        }

        # 3. Enviar asíncronamente
        background_tasks.add_task(send_to_elastic, elastic_data)
        
        return {
            "status": "success",
            "user": username,
            "repository_count": len(repositories),
            "data": repositories[:5],  # Muestra solo los primeros 5 para la respuesta
            "message": "Repositorios procesados exitosamente"
        }

    except HTTPException as he:
        logger.warning(f"Error controlado: {he.detail}")
        raise
    except Exception as e:
        logger.error(f"Error inesperado procesando {username}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error procesando repositorios: {str(e)}"
        )