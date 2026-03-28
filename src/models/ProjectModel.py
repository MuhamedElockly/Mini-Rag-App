

from .BaseDataModel import BaseDataModel


from .db_schemas.project import Project
from .Enums.DataBaseEnum import DataBaseEnum
class ProjectModel(BaseDataModel):
    def __init__(self,db_client:object):
        super().__init__(db_client=db_client)
        self.collection=self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]

    async def create_project(self,project:Project):
        project_dict=project.dict()
        result=await self.collection.insert_one(project_dict)
        project._id=result.inserted_id
        return project
    async def get_project_or_create_one(self,projct_id:str):
        record=await self.collection.find_one(
            {"project_id":projct_id}
        )
        if record is None:
            project=Project(project_id=projct_id)
            project= await self.create_project(project)
            return project
        return Project(**record)

    async def get_all_projects(self,page:int=1,page_size:int=10):
        total_records=await self.collection.count_documents({})
        total_pages=(total_records+page_size-1)//page_size
        skip=(page-1)*page_size
        cursor=self.collection.find().skip(skip).limit(page_size)
        projects=[]
        async for record in cursor:
            projects.append(Project(**record))
        return projects, total_pages