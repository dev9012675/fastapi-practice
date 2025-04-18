from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    dbms:str
    database_hostname:str
    database_port:str
    database_name:str
    database_username:str
    database_password:str
    secret_key:str
    algorithm:str
    access_token_expire_minutes:int
    allowed_origins:str

    class Config:
        env_file = ".env"

settings = Settings()

