from fastapi import APIRouter, HTTPException, BackgroundTasks
from Services.user_service import GithubUserService
from Elastic.elastic_client import es  
from elasticsearch.helpers import async_bulk

router = APIRouter()

async def send_to_elastic(repos: list):
    try:
        actions = [
            {"_index": "github_repos", "_source": repo}
            for repo in repos
        ]
        await async_bulk(es, actions)
    except Exception as e:
        print(f"Error en Elasticsearch: {e}")

@router.get("/user/{username}/repos")
async def get_user_repos(username: str, background_tasks: BackgroundTasks):
    try:
        repos = GithubUserService.get_user_repos_info(username)
        background_tasks.add_task(send_to_elastic, repos)  # Envía datos en segundo plano
        return {"username": username, "repos": repos}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))