from pydantic import BaseSettings


class Settings(BaseSettings):
    # Traffic Data Access Keys
    tom_tom_access_key: str
    database_url: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


SETTINGS = Settings()
