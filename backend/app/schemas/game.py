from datetime import datetime

from pydantic import BaseModel


class GameStartConfig(BaseModel):
    player_name: str
    repo_name: str
    repo_owner: str
    repo_branch: str


class GameInfo(BaseModel):
    game_id: int
    repo_id: int
    player_name: str
    start_time: datetime

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
