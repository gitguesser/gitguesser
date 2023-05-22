import sys

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Loads configuration of the application.

    When an instance of this class is created, its attributes are
    initialized using the values from both environment variables and
    the content of .env file.
    """
    postgres_user: str
    postgres_password: str
    postgres_server: str
    postgres_port: int
    postgres_db: str
    github_username: str | None
    github_token: str | None

    class Config:
        case_sensitive = False
        env_file = ".env" if "pytest" not in sys.modules else ".env.test"
        env_file_encoding = "utf-8"


settings = Settings()
