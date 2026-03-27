from pydantic import BaseModel, Field
from typing import Optional
from bson.objectid import ObjectId

class DataChunk(BaseModel):
    _id: Optional[ObjectId]
    chunk_text: str=Field(...,min_length=1)
    chunk_project_id: ObjectId
    chunk_order: int=Field(...,gt=0)
    chunk_metadata: dict

    class Config:
        arbitrary_types_allowed = True

