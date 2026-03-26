

from .BaseController import BaseController
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
    
    