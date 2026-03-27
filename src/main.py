from fastapi import FastAPI
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings, Settings

load_dotenv(".env")
from routes import base,data
app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    settings=get_settings()
    app.mongodb_client=AsyncIOMotorClient(settings.MONGO_URL)
    app.db_client=app.mongodb_client[settings.MONGO_DB_NAME]
@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()
# app.include_router(base.baseRouter)
app.include_router(data.baseRouter)

