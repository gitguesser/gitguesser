from datetime import datetime
from typing import List

from pydantic import BaseModel


class RepoId(BaseModel):
    name: str
    owner: str


class GameId(BaseModel):
    id: int


class GameResults(BaseModel):
    game_id: int
    repo_name: str
    repo_owner: str
    start_time: datetime
    end_time: datetime
    score: int
    player_answer: str
    correct_answer: str

    class Config:
        orm_mode = True


class FolderContent(BaseModel):
    tree_id: str
    name: str
    content: List[str]


class PlayerAnswer(BaseModel):
    answer: str
