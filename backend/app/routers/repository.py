from app.dependencies import get_session
from fastapi import APIRouter, Depends
from schemas.repository import Directory
from sqlalchemy.orm import AsyncSession

router = APIRouter(
    prefix="/repository",
    tags=["repository"],
)


@router.get(
    "/{id}/tree",
    response_model=Directory,
    description="Returns root directory of the repository with given id.",
)
async def get_root_directory(id: int, session: AsyncSession = Depends(get_session)):
    root_directory = repository_service.get_root_directory(db=session, repo_id=id)
    return root_directory


@router.get(
    "/{id}/tree/{directory_id}",
    response_model=Directory,
    description="Returns directory with given id that belongs to the repository.",
)
async def get_directory(
    id: int, directory_id: str, session: AsyncSession = Depends(get_session)
):
    directory = repository_service.get_directory(
        db=session, repo_id=id, directory_id=directory_id
    )
    return directory
