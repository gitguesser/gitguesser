import datetime

from app.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    repository_id = Column(Integer, ForeignKey("repositories.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    player_name = Column(String, nullable=False)
    correct_answer = Column(String, nullable=False)
    player_answer = Column(String)
    score = Column(Integer)

    repository = relationship("Repository", back_populates="games")


class Repository(Base):
    __tablename__ = "repositories"
    __table_args__ = (Index("idx_name_owner", "name", "owner"),)

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    owner = Column(String, nullable=False)
    branch = Column(String, nullable=False)
    etag = Column(String, nullable=False)
    data = Column(JSONB, nullable=False)
    creation_date = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)

    games = relationship("Game", back_populates="repository")
