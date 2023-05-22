from fastapi import APIRouter
from app.schemas.game import GameInfo, GameResults, GameStartConfig, PlayerAnswer

router = APIRouter(
    prefix="/game",
    tags=["game"],
)


@router.post(
    "/",
    response_model=GameInfo,
    description="Starts a new game.",
)
async def start_game(game_start_config: GameStartConfig):
    pass


@router.get(
    "/{id}",
    response_model=GameInfo,
    description="Retrieves information about a game with given id.",
)
async def get_game_info(id: int):
    pass


@router.get(
    "/{id}/results",
    response_model=GameResults,
    description="Retrieves results of finished game with given id.",
)
async def get_game_results(id: int):
    pass


@router.post("/{id}", description="Sends player answer for a game with given id.")
async def send_answer(id: int, answer: PlayerAnswer):
    pass
