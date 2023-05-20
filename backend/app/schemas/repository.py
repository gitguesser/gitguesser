from pydantic import BaseModel


class DirectoryInfo(BaseModel):
    id: str
    name: str


class Directory(DirectoryInfo):
    subdirectories: list[DirectoryInfo]
