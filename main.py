from fastapi import FastAPI
from Routers.router_user import router as user_router

app = FastAPI()

# Registrar routers
app.include_router(user_router, prefix="/github", tags=["Users"])
