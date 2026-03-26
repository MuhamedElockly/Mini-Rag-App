from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv(".env")
from routes import base,data
app = FastAPI()
app.include_router(base.baseRouter)
app.include_router(data.baseRouter)

