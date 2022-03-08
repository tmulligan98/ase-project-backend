from pydantic import BaseSettings


class Settings(BaseSettings):
    # Traffic Data Access Keys
    tom_tom_access_key: str
    database_url: str
    auth_secret_key: str
    crypto_algorithm: str
    auth_access_token_expire_minutes: int = int(30)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


SETTINGS = Settings()
