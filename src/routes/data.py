from fastapi import APIRouter, FastAPI,Depends,UploadFile,status
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
from controllers import DataController, ProjectController
import os
baseRouter = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1","data"]
)

@baseRouter.post("/upload/{project_id}")
async def upload_file(project_id: str, file: UploadFile):
    is_valid , res_message = DataController().validate_file(file=file)
    if not is_valid:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": res_message.value})

    project_path = ProjectController().get_project_path(project_id=project_id)
    
    return JSONResponse(status_code=status.HTTP_200_OK, content={"Message":res_message.value})