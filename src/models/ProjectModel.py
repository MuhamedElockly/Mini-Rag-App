

from .BaseDataModel import BaseDataModel


from .db_schemas.project import Project
from .Enums.DataBaseEnum import DataBaseEnum
class ProjectModel(BaseDataModel):
    def __init__(self,db_client:object):
        super().__init__(db_client=db_client)
        self.collection=self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]

    async def init_collection(self):
        all_collections =await self.db_client.list_collection_names();
        if DataBaseEnum.COLLECTION_PROJECT_NAME.value not in all_collections:
           self.collection= self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]
           indexes=  Project.get_indexes()
           for index in indexes:
               await self.collection.create_index(
                   index["key"],
                   name=index["name"],
                   unique=index["unique"]
               )
    @classmethod
    async def create_instance(cls,db_client:object):
        instance=cls(db_client=db_client)
        await instance.init_collection()
        return instance




    async def create_project(self,project:Project):
        project_dict=project.dict(by_alias=True,exclude_unset=True)
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