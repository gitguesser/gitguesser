from app.dependencies import get_session
from app.schemas.game import (
    GameInfo,
    GameResults,
    GameStartConfig,
    GameWithId,
    PlayerAnswer,
)
from app.services import game_service
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/game",
    tags=["game"],
)


@router.post(
    "/",
    response_model=GameWithId,
    description="Starts a new game.",
)
async def start_game(
    game_start_config: GameStartConfig, session: AsyncSession = Depends(get_session)
):
    game_id = await game_service.start_game(db=session, game_config=game_start_config)
    return {"game_id": game_id}


@router.get(
    "/{id}",
    response_model=GameInfo,
    description="Retrieves information about a game with given id.",
)
async def get_game_info(id: int, session: AsyncSession = Depends(get_session)):
    game = await game_service.get_game(db=session, game_id=id)
    return game


@router.get(
    "/{id}/results",
    response_model=GameResults,
    description="Retrieves results of finished game with given id.",
)
async def get_game_results(id: int, session: AsyncSession = Depends(get_session)):
    game = await game_service.get_game_answered(db=session, game_id=id)
    return game


@router.post("/{id}", description="Sends player answer for a game with given id.")
async def send_answer(
    id: int, answer: PlayerAnswer, session: AsyncSession = Depends(get_session)
):
    await game_service.give_answer(db=session, game_id=id, answer=answer.answer)
    return
