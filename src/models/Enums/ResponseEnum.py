from enum import Enum

class ResponseEnum(Enum):
    FILE_VALIDATION_ERROR = "file_validation_error"
    FILE_VALIDATION_SUCCESS = "file_validation_success"
    FILE_TYPE_NOT_ALLOWED = "file_type_not_allowed"
    FILE_SIZE_EXCEEDED = "file_size_exceeded"
    FILE_UPLOAD_SUCCESS = "file_upload_success"
    FILE_UPLOAD_FAILED = "file_upload_failed"
    FILE_PROCESSING_FAILED = "file_processing_failed"
    FILE_PROCESSING_SUCCESS = "file_processing_success"

