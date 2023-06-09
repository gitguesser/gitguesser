from pydantic import BaseModel


class DirectoryInfo(BaseModel):
    id: str
    name: str


class Directory(DirectoryInfo):
    subdirectories: list[DirectoryInfo]


class Repository(BaseModel):
    id: int
    name: str
    owner: str
    branch: str

    class Config:
        orm_mode = True
