from fastapi import APIRouter, HTTPException, BackgroundTasks
from Services.template_service import FileCheckService
from Models.template_check import TemplateCheckResult
from Elastic.index_dispatcher import send_document
import logging
from datetime import datetime

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/users/{user_or_org}/check-pull-request-templates")
async def check_pull_request_templates(user_or_org: str, background_tasks: BackgroundTasks):
    try:
        if not user_or_org:
            raise HTTPException(status_code=400, detail="User/org name is required")

        result = await FileCheckService.analyze_pull_request_template(user_or_org)

        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        if not result.get("repositories"):
            raise HTTPException(status_code=404, detail="No repositories found to analyze")

        result["timestamp"] = datetime.utcnow().isoformat()
        template_result = TemplateCheckResult(**result)
        doc_id = f"{user_or_org}_{int(datetime.utcnow().timestamp())}"

        background_tasks.add_task(send_document, "github_template", doc_id, template_result)

        return {
            "status": "success",
            "user": user_or_org,
            "stats": result.get("stats"),
            "sample_data": result["repositories"][:5]
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
