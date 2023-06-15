from pydantic import BaseModel


class Repository(BaseModel):
    name: str
    owner: str
    branch: str


class Repositories(BaseModel):
    repos: list[Repository]
