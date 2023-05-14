from fastapi import APIRouter
from schemas.repository import Directory
from services import (
    get_directory as get_directory_service,
    get_root_directory as get_root_directory_service,
)
from app.dependencies import get_session


router = APIRouter(
    prefix="/repository",
    tags=["repository"],
)


@router.get(
    "/{id}/tree",
    response_model=Directory,
    description="Returns root directory of the repository with given id.",
)
async def get_root_directory(id: int):
    async with get_session() as session:
        root_directory =  get_root_directory_service(db = session, repo_id = id)
    return root_directory


@router.get(
    "/{id}/tree/{directory_id}",
    response_model=Directory,
    description="Returns directory with given id that belongs to the repository.",
)
async def get_directory(id: int, directory_id: str):
    async with get_session() as session:
        directory = get_directory_service( db = session, repo_id = id, directory_id = directory_id)
    return directory
