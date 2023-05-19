from pydantic import BaseSettings

class Settings(BaseSettings):
    MESSAGE_SERVICE : str
    TARGET : str
    API_BEARER : str


    class Config:
        env_file = '.env'

config = Settings()