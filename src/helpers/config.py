from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    App_NAME: str 
    App_VERSION: str
    APP_DESCRIPTION: str
    OPENAI_API_KEY: str
    FILE_ALLOWED_EXTENSIONS: list
    FILE_MAX_SIZE_MB: int
    # python-dotenv: str
 
    class Config:
        env_file = ".env"
    
def get_settings():
    return Settings()