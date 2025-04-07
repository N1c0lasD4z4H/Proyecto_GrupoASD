from fastapi import FastAPI
from Routers.user_rputer import router as user_router
from Routers.org_router import router as org_router
from Routers.pr_router import router as pr_router
from Routers.activity_router import router as activity_router
from Routers.template_router import router as template_router
from Routers.get_rcommits_repo import router as get_rcommits_repo

app = FastAPI()
#Routers
app.include_router(user_router, prefix="/github", tags=["Repositories Users"])
app.include_router(org_router, prefix="/github", tags=["Organizations"])
app.include_router(pr_router, prefix="/github", tags=["Pull request"])
app.include_router(activity_router, prefix="/github", tags=["Activity user"])
app.include_router(template_router, prefix="/github",tags=["Template General"])
app.include_router(get_rcommits_repo, prefix="/github",tags=["Repositories Commits"])