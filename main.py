from fastapi import FastAPI
from Routers.user_rputer import router as user_router
from Routers.pr_router import router as pr_router
from Routers.pr_time_router import router as pr_time_router
from Routers.activity_router import router as activity_router
from Routers.template_router import router as template_router
from Routers.repo_activity_router import router as repo_activity_router
from Routers.issue_router import router as issue_router
app = FastAPI()
#Routers

app.include_router(user_router, prefix="/github", tags=["Repositories Users"])
app.include_router(repo_activity_router, prefix="/github", tags=["Repo Activity"])
app.include_router(activity_router, prefix="/github", tags=["Activity user"])
app.include_router(pr_router, prefix="/github", tags=["Pull request labels"])
app.include_router(pr_time_router, prefix="/github", tags=["Pull request time"])
app.include_router(issue_router, prefix="/github", tags=["Issues"])
app.include_router(template_router, prefix="/github",tags=["Template General"])
