from fastapi import APIRouter
from schemas.repository import Directory

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
    pass


@router.get(
    "/{id}/tree/{directory_id}",
    response_model=Directory,
    description="Returns directory with given id that belongs to the repository.",
)
async def get_directory(id: int, directory_id: str):
    pass
