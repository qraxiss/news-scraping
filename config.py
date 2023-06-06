from pydantic import BaseSettings


class Settings(BaseSettings):
    SITE: str

    TELEGRAM_API_BEARER: str
    TELEGRAM_API_URI: str

    AI_ANALYSIS_API_URI: str

    CRHOME_DRIVER: str

    WORDPRESS_API_URI: str

    class Config:
        env_file = '.env'


config = Settings()
