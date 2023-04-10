from pydantic import BaseModel


class DirectoryInfo(BaseModel):
    directory_id: str
    name: str


class Directory(DirectoryInfo):
    subdirectories: list[DirectoryInfo]
