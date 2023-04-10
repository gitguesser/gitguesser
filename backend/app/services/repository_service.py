from app.models.repository import Repository
from app.schemas.repository import Directory
from sqlalchemy.ext.asyncio import AsyncSession


async def update_repo(*, db: AsyncSession, owner: str, repo: str) -> Repository:
    """Saves the repository's tree to the database and returns its id.

    If the repository's tree is already saved, then it checks if the newest one has
    been updated since saving it (using ETag). If there are any updates, it saves
    a new copy to the database.
    """


async def get_repo(*, db: AsyncSession, repo_id: str) -> Repository:
    """Returns repository with given id or raises HTTPException if it does not exist."""


async def get_directory(
    *, db: AsyncSession, repo_id: str, directory_id: str
) -> Directory:
    """Returns the directory with given id that belongs to the repository.

    Raises HTTPException if the repository does not exist or it does not contain
    this directory.
    """


async def get_root_directory(*, db: AsyncSession, repo_id: str) -> Directory:
    """Returns the root directory of the repository with given id.

    Raises HTTPException if the repository does not exist.
    """


async def get_random_file_path(*, db: AsyncSession, repo_id: str) -> str:
    """Returns path to a randomly selected file that belongs to the repository.

    Raises HTTPException if the repository does not exist.
    The returned path is in the format 'a/b/c/file.txt'.
    """
