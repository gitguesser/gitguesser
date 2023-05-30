from app.dependencies import get_session
from fastapi import APIRouter, Depends
from app.schemas.repository import Directory, Repository
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import repository_service

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
    root_directory = await repository_service.get_root_directory(db=session, repo_id=id)
    return root_directory


@router.get(
    "/{id}/tree/{directory_id}",
    response_model=Directory,
    description="Returns directory with given id that belongs to the repository.",
)
async def get_directory(
    id: int, directory_id: str, session: AsyncSession = Depends(get_session)
):
    directory = await repository_service.get_directory(
        db=session, repo_id=id, directory_id=directory_id
    )
    return directory


@router.get(
    "/{id}",
    response_model=Repository,
    description="Returns information about a repository with given id.",
)
async def get_repository(id: int, session: AsyncSession = Depends(get_session)):
    repository = await repository_service.get_repo(db=session, repo_id=id)
    return repository
