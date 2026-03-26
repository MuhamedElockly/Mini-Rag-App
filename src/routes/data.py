from fastapi import APIRouter, FastAPI,Depends,UploadFile,status
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
from controllers import DataController, ProjectController
import os
from models import ResponseEnum
import aiofiles
import logging

logger= logging.getLogger('uvicorn.error')

baseRouter = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1","data"]
)

@baseRouter.post("/upload/{project_id}")
async def upload_file(project_id: str, file: UploadFile):
    data_controller = DataController()
    is_valid , res_message = data_controller.validate_file(file=file)
    if not is_valid:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": res_message.value})

    project_path = ProjectController().get_project_path(project_id=project_id)
    file_path,file_id = data_controller.generate_unique_file_path(filename=file.filename, project_id=project_id)
    try :
        async with aiofiles.open(file_path+file_id, 'wb') as f:
            while chunk := await file.read(get_settings().FiLE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": ResponseEnum.FILE_UPLOAD_FAILED.value, "error": str(e)})

    return JSONResponse( content={"Message":    ResponseEnum.FILE_UPLOAD_SUCCESS.value})