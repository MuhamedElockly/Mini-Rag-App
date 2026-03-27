import os
from .BaseController import BaseController
from .ProjectController import ProjectController
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from models import ProcessingEnum
class ProcessController(BaseController):
    def __init__(self,project_id:str):
        super().__init__()
        self.project_id=project_id
        self.project_path=ProjectController().get_project_path(project_id=project_id)

    def get_file_extension(self,file_id:str):
        return os.path.splitext(file_id)[-1]
    
    def get_file_loader(self,file_id:str):
        file_extension=self.get_file_extension(file_id=file_id)
        file_path=os.path.join(self.project_path, file_id)
        if file_extension in ProcessingEnum.TXT.value: 
            return TextLoader(file_path,encoding='utf-8')
        elif file_extension in ProcessingEnum.PDF.value:
            return PyPDFLoader(file_path)
        else:
            return None
    def get_file_content(self,file_id:str):
        loader=self.get_file_loader(file_id=file_id)
        if loader is None:
            raise ValueError(f"Unsupported file type for file_id: {file_id}")
        documents=loader.load()
        return documents
    def process_file_content(self,file_id:str,file_content:list,chunk_size:int=1000,chunk_overlap:int=200):
        text_splitter=RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len
            )
        file_content_text=[doc.page_content for doc in file_content]
        file_content_metadata=[doc.metadata for doc in file_content]
        chunks=text_splitter.create_documents(file_content_text,metadatas=file_content_metadata)
        return chunks