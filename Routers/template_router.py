from fastapi import APIRouter, HTTPException
from Services.template_service import FileCheckService

router = APIRouter()

@router.get("/users/{user_or_org}/check-pull-request-templates")
async def check_pull_request_templates(user_or_org: str):
    """
    Verifica los repositorios de un usuario u organización para identificar la presencia de la plantilla del pull request.
    """
    try:
        result = FileCheckService.analyze_pull_request_template(user_or_org)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
