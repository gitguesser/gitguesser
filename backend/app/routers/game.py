from fastapi import APIRouter
from schemas.game import *

router = APIRouter(
    prefix="/game",
    tags=["game"],
)


@router.post(
    "/",
    response_model=GameId,
    description="Retrieves information about a finished game with given id.",
)
async def start_game(repo_id: RepoId):
    pass


@router.get(
    "/{id}/results",
    response_model=GameResults,
    description="Retrieves information about a finished game with given id.",
)
async def get_game_results(id: int):
    pass


@router.get(
    "/{id}/tree",
    response_model=FolderContent,
    description="Retrieves list of folders in root folder in repository used in game with given id.",
)
async def get_root_folder_content(id: int):
    pass


@router.get(
    "/{game_id}/tree/{tree_id}",
    response_model=FolderContent,
    description="Retrieves list of folders in tree_id folder in repository used in game with given game_id.",
)
async def get_folder_content(game_id: int, tree_id: str):
    pass


@router.post("/{id}", description="Sends player answer for a game with given id.")
async def send_answer(id: int, answer: PlayerAnswer):
    pass
