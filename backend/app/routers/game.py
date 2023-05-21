import services.game_service
import services.repository_service
from app.dependencies import get_session
from fastapi import APIRouter, Depends
from schemas.game import (
    Game,
    GameInfo,
    GameResults,
    GameStartConfig,
    PlayerAnswer,
    Repository,
)
from sqlalchemy.orm import AsyncSession

router = APIRouter(
    prefix="/game",
    tags=["game"],
)


@router.post(
    "/",
    response_model=Game,
    description="Starts a new game.",
)
async def start_game(
    game_start_config: GameStartConfig, session: AsyncSession = Depends(get_session)
):
    game_id = services.game_service.start_game(
        db=session, game_config=game_start_config
    )
    return game_id


@router.get(
    "/{id}",
    response_model=GameInfo,
    description="Retrieves information about a game with given id.",
)
async def get_game_info(id: int, session: AsyncSession = Depends(get_session)):
    game = await services.game_service.get_game(db=session, game_id=id)
    return game


@router.get(
    "/{id}/results",
    response_model=GameResults,
    description="Retrieves results of finished game with given id.",
)
async def get_game_results(id: int, session: AsyncSession = Depends(get_session)):
    game = await services.game_service.get_game(db=session, game_id=id)
    return game


@router.post("/{id}", description="Sends player answer for a game with given id.")
async def send_answer(
    id: int, answer: PlayerAnswer, session: AsyncSession = Depends(get_session)
):
    services.game_service.give_answer(db=session, game_id=id, answer=answer)
    return


@router.get(
    "/{id}",
    response_model=Repository,
    description="Returns information about a repository with given id.",
)
async def get_repository(id: int, session: AsyncSession = Depends(get_session)):
    repository = services.repository_service.get_repo(db=session, repo_id=id)
    return repository
