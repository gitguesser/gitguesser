from datetime import datetime
from typing import List

from pydantic import BaseModel


class GameStartConfig(BaseModel):
    player_name: str
    repo_name: str
    repo_owner: str


class GameInfo(BaseModel):
    game_id: int
    player_name: str
    repo_name: str
    repo_owner: str
    start_time: datetime


class GameResults(GameInfo):
    end_time: datetime
    score: int
    player_answer: str
    correct_answer: str

    class Config:
        orm_mode = True


class FolderInfo(BaseModel):
    tree_id: str
    name: str
    content: List[str]


class PlayerAnswer(BaseModel):
    answer: str
