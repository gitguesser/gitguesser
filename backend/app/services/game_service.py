from app.models.game import Game
from sqlalchemy.ext.asyncio import AsyncSession


async def start_game(*, db: AsyncSession, game_config: GameStartConfig) -> int:
    """Starts a game based on data in game_config and returns its id."""


async def get_game(*, db: AsyncSession, game_id: int) -> Game:
    """Returns the game with given id or raises a 404 HTTPException if it does not exist."""


async def give_answer(*, db: AsyncSession, game_id: int, answer: str) -> None:
    """Gives answer to the game with given id.

    If the game does not exist, raises a 404 HTTPException. If it has already
    ended, nothing happens.
    The score is calculated as the distance (in directories tree) between
    user's answer and the correct answer (lower score is better).
    """
