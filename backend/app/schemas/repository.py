from pydantic import BaseModel


class DirectoryInfo(BaseModel):
    id: str
    name: str


class Directory(DirectoryInfo):
    subdirectories: list[DirectoryInfo]


class Repository(BaseModel):
    repo_id: int
    repo_name: str
    repo_owner: str
    repo_branch: str
