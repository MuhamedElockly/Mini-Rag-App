from urllib import request

from fastapi import APIRouter, FastAPI,Depends,UploadFile,status,Request
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
from controllers import DataController, ProjectController,ProcessController
import os
from models import ResponseEnum
import aiofiles
import logging

from models.db_schemas import DataChunk
from .schemas.data import ProcessRequest
from models import ProjectModel
from models.ChunkModel import ChunkModel


logger= logging.getLogger('uvicorn.error')

baseRouter = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1"]
)

@baseRouter.post("/upload/{project_id}")
async def upload_file(request:Request,project_id: str, file: UploadFile):

    project_model=await ProjectModel.create_instance(db_client=request.app.db_client)
    project=await project_model.get_project_or_create_one(projct_id=project_id)


    data_controller = DataController()
    is_valid , res_message = data_controller.validate_file(file=file)
    if not is_valid:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": res_message.value})

    project_path = ProjectController().get_project_path(project_id=project_id)
    file_path,file_id = data_controller.generate_unique_file_path(filename=file.filename, project_id=project_id)
    print(f"Generated file path: {file_path}, file_id: {file_id}")
    full_destination = os.path.join(file_path, file_id)
    try :
        async with aiofiles.open(full_destination, 'wb') as f:
            while chunk := await file.read(get_settings().FiLE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}")
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": ResponseEnum.FILE_UPLOAD_FAILED.value, "error": str(e)})

    return JSONResponse(
         content={
             "Message": ResponseEnum.FILE_UPLOAD_SUCCESS.value ,
             "File_Id": file_id,
            
             })

@baseRouter.post("/process/{project_id}")
async def process_endpoint(request:Request,project_id: str, processRequest:ProcessRequest):

    
    project_model=await ProjectModel.create_instance(db_client=request.app.db_client)
    project=await project_model.get_project_or_create_one(projct_id=project_id)


    file_id=processRequest.file_id
    chunk_size=processRequest.chunk_size
    overlap_size=processRequest.overlap_size
    do_reset=processRequest.do_reset
    process_controller=ProcessController(project_id=project_id)
    file_content=process_controller.get_file_content(file_id=file_id)
    chunks=process_controller.process_file_content(file_id=file_id,file_content=file_content,chunk_size=chunk_size,chunk_overlap=overlap_size)
   


    file_chunks_records=[DataChunk(
        chunk_text=chunk.page_content,
        chunk_metadata=chunk.metadata,
        chunk_order=i+1,
        chunk_project_id=project.id
    ) for i, chunk in enumerate(chunks)]

    chunk_model=await ChunkModel.create_instance(db_client=request.app.db_client)
    if do_reset:
        deleted_count =await chunk_model.delete_chunks_by_project_id(project_id=project.id)
    no_records=await chunk_model.insert_many_chunks(chunks=file_chunks_records)
    return JSONResponse(
        content={
            "message":ResponseEnum.FILE_PROCESSING_SUCCESS.value,
            "file_id":file_id,
            "total_chunks":no_records,
            "deleted_chunks":deleted_count if do_reset else 0
        }
    )