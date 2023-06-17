from datetime import datetime

from pydantic import BaseModel


class GameWithId(BaseModel):
    game_id: int


class GameStartConfig(BaseModel):
    player_name: str
    repo_name: str
    repo_owner: str
    repo_branch: str


class GameInfo(BaseModel):
    id: int
    repository_id: int
    player_name: str
    start_time: datetime
    file_name: str

    class Config:
        orm_mode = True


class GameResults(GameInfo):
    end_time: datetime
    score: int
    player_answer: str
    correct_answer: str

    class Config:
        orm_mode = True


class PlayerAnswer(BaseModel):
    answer: str
