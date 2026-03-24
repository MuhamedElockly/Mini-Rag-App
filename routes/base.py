from fastapi import APIRouter, FastAPI
import os
baseRouter = APIRouter(
    prefix="/api/v1",
    tags=["base"]
)

@baseRouter.get("/welcome")
async def welcome():
    app_name=os.getenv("APP_NAME")
    app_version=os.getenv("APP_VERSION")
    return {"message": f"Welcome to {app_name} {app_version}!"}