from pydantic import BaseSettings


class Settings(BaseSettings):
    # Traffic Data Access Keys
    tom_tom_access_key: str
    heroku_postgres_uri: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


SETTINGS = Settings()
