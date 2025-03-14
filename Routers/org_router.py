from fastapi import APIRouter, HTTPException
from Services.org_service import GithubOrgService

router = APIRouter()

@router.get("/org/{org_name}/repos")
async def get_org_repos(org_name: str):
    try:
        repos = GithubOrgService.get_org_repos_info(org_name)
        return {"organization": org_name, "repos": repos}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
