from pydantic import BaseSettings


class Settings(BaseSettings):
    # Traffic Data Access Keys
    tom_tom_access_key: str


SETTINGS = Settings()
