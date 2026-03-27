
import os
import re
from .BaseController import BaseController
from .ProjectController import ProjectController
from fastapi import UploadFile
from models import ResponseEnum
class DataController(BaseController):
    def __init__(self):
        super().__init__()
        self.size_scale = 1024 * 1024  
    def validate_file(self,file:UploadFile):
        if file.content_type not in self.app_settings.FILE_ALLOWED_EXTENSIONS:
            return False ,ResponseEnum.INVALID_FILE_TYPE
        if file.size > (self.app_settings.FILE_MAX_SIZE_MB * self.size_scale):
            return False ,ResponseEnum.FILE_SIZE_EXCEEDED
        return True , ResponseEnum.FILE_VALIDATION_SUCCESS
    
    def generate_unique_file_path(self,filename:str,project_id:str):
        random_name= self.generate_random_string(length=12)
        # random_name=filename
        project_path=ProjectController().get_project_path(project_id=project_id)
        clean_filename=self.get_clean_filename(filename=filename)
        # new_file_path=os.path.join(project_path,random_name+"_"+clean_filename)
        
        return project_path, random_name+"_"+clean_filename
    def get_clean_filename(self,filename:str):
        #remove file extension to use later for generating unique file name
        extension=os.path.splitext(filename)[-1]
        filename = os.path.splitext(filename)[0]
        # remove any special characters and replace spaces with underscores
        cleaned_filename = re.sub(r'[^\w\s-]', '', filename)

        cleaned_filename=cleaned_filename.replace(' ', '_')
        # add the extension back to the cleaned filename
        cleaned_filename += extension
        return cleaned_filename