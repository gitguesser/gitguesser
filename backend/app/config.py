from pydantic import BaseSettings


class Settings(BaseSettings):
    """Loads configuration of the application.

    When an instance of this class is created, its attributes are
    initialized using the values from both environment variables and
    the content of .env file.
    """

    # We don't provide this values currently and our app won't start without them
    # postgres_user: str
    # postgres_password: str
    # postgres_server: str
    # postgres_port: int
    # postgres_db: str
    database_url: str
    frontend_url: str

    class Config:
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
