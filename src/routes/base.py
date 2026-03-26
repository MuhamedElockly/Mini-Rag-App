from fastapi import APIRouter, FastAPI,Depends
from helpers.config import get_settings, Settings
import os
baseRouter = APIRouter(
    prefix="/api/v1",
    tags=["base"]
)

@baseRouter.get("/welcome")
async def welcome(app_settings: Settings = Depends(get_settings)):
    app_name = app_settings.App_NAME
    app_version = app_settings.App_VERSION
    return {"message": f"Welcome to {app_name} {app_version}!"}