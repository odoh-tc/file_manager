from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_HOST: str
    MYSQL_PORT: str
    MYSQL_DB_NAME: str
    MYSQL_TEST_DB_NAME: str
    BASE_URL: str
    MYSQL_ROOT_PASSWORD: str
    TESTING: bool


    class Config:
        env_file = ".env"

settings = Settings()
