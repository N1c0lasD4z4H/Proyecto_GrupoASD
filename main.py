from fastapi import FastAPI
from Routers.user_rputer import router as user_router
from Routers.org_router import router as org_router
from Routers.pr_router import router as pr_router
app = FastAPI()

#Routers
app.include_router(user_router, prefix="/github", tags=["Users"])
app.include_router(org_router, prefix="/github", tags=["Organizations"])
app.include_router(pr_router, prefix="/github", tags=["Pull request"])
