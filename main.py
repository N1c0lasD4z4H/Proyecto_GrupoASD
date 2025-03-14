from fastapi import FastAPI
from Routers.router_user import router as user_router
from Routers.org_router import router as org_router

app = FastAPI()

# Registrar routers
app.include_router(user_router, prefix="/github", tags=["Users"])
app.include_router(org_router, prefix="/github", tags=["Organizations"])
