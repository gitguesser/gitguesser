from fastapi import APIRouter
from schemas.game import GameInfo, GameResults, GameStartConfig, PlayerAnswer
import services.game_service
import services.repository_service
from services.game_service import start_game as start_game_service
from services.game_service import get_game as get_game_service
from services.game_service import give_answer as give_answer_service
from app.dependencies import get_session

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
    async with get_session() as session:
        game_id = services.game_service.start_game(db = session, game_config = game_start_config)
    return game_id


@router.get(
    "/{id}",
    response_model=GameInfo,
    description="Retrieves information about a game with given id.",
)
async def get_game_info(id: int):
    async with get_session() as session:
        game = await services.game_service.get_game(db = session, game_id = id)
        repo = await repository_service.get_repo(db = session, repo_id = game.repository_id)

        game_info = GameInfo(
            game_id = id,
            repo_id = repo.id,
            player_name = game.player_name,
            repo_name = repo.name,
            repo_owner = repo.owner,
            start_time = game.start_time,
        )
    return game_info
    

@router.get(
    "/{id}/results",
    response_model=GameResults,
    description="Retrieves results of finished game with given id.",
)
async def get_game_results(id: int):
    async with get_session() as session:
        game_info = await get_game_info(id)
        game = await game_service.get_game(db = session, game_id=id)

        game_result = GameResults(
            **dict(game_info), 
            end_time = game.end_time, 
            score = game.score, 
            player_answer = game.player_answer,
            correct_answer = game.correct_answer
        ) 
    return game_result


@router.post("/{id}", description="Sends player answer for a game with given id.")
async def send_answer(id: int, answer: PlayerAnswer):
    async with get_session() as session:
        game_service.give_answer(db=session, game_id=id, answer=answer)
    return
