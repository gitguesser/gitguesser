import datetime

from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import Game
from app.schemas.game import GameStartConfig
from .repository_service import get_random_file_path, update_repo


async def start_game(*, db: AsyncSession, game_config: GameStartConfig) -> int:
    """Starts a game based on data in game_config and returns its id."""
    repo_id = await update_repo(
        db=db,
        owner=game_config.repo_owner,
        name=game_config.repo_name,
        branch=game_config.repo_branch,
    )

    correct_answer = await get_random_file_path(db=db, repo_id=repo_id)

    game = Game(
        repository_id=repo_id,
        start_time=datetime.datetime.utcnow(),
        player_name=game_config.player_name,
        correct_answer=correct_answer,
    )
    db.add(game)
    await db.commit()

    return game.id


async def get_game(*, db: AsyncSession, game_id: int) -> Game:
    """Returns the game with given id or raises a 404 HTTPException if it does not exist."""
    game = await db.scalar(select(Game).where(Game.id == int(game_id)))
    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")

    return game


async def give_answer(*, db: AsyncSession, game_id: int, answer: str) -> None:
    """Gives answer to the game with given id.

    If the game does not exist, raises a 404 HTTPException. If it has already
    ended, nothing happens.
    The score is calculated as the distance (in directories tree) between
    user's answer and the correct answer (lower score is better).
    """
    game = await get_game(db=db, game_id=game_id)

    if game.end_time is not None:
        return

    correct_path = game.correct_answer.split("/")[:-1]
    player_path = answer.split("/")[:-1]

    min_len = min(len(correct_path), len(player_path))
    i = 0
    while i < min_len and correct_path[i] == player_path[i]:
        i += 1
    score = len(correct_path) + len(player_path) - 2 * i

    await db.execute(
        update(Game)
        .where(Game.id == int(game_id))
        .values(
            dict(score=score, end_time=datetime.datetime.utcnow(), player_answer=answer)
        )
    )
