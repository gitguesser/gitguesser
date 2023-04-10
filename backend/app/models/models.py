from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    repo_id = Column(Integer, ForeignKey("repos.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    player_name = Column(String, nullable=False)
    correct_answer = Column(String, nullable=False)
    player_answer = Column(String)
    score = Column(Integer)

    repo = relationship("Repo", back_populates="games")


class Repo(Base):
    __tablename__ = "repos"

    # TODO Add repo owner and repo name or link to repo.
    id = Column(Integer, primary_key=True, index=True)
    ETag = Column(String, nullable=False)
    data = Column(JSONB, nullable=False)

    games = relationship("Game", back_populates="repo")
