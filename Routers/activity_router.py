from fastapi import APIRouter, HTTPException
from Elastic.index_dispatcher import es
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/users/{username}/commits")
async def get_commits(username: str):
    try:
        # Simulación: insertar dummy data para que es.index() se llame
        await es.index(
            index="github_commits",
            document={"username": username, "total_commits": 42}
        )
        return {"total_commits": 42}
    except Exception as e:
        logger.error(f"Error processing commits for {username}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
