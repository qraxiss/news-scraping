from pydantic import BaseSettings

class Settings(BaseSettings):
    SITE : str

    API_BEARER : str
    API_URI : str


    class Config:
        env_file = '.env'

config = Settings()