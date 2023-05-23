import random

import httpx
from fastapi import HTTPException, status
from sqlalchemy import func, literal_column, select
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.models import Repository
from ..schemas.repository import Directory, DirectoryInfo


async def update_repo(*, db: AsyncSession, owner: str, name: str, branch: str) -> int:
    """Saves the repository in the database and returns its id.

    If the repository is already saved, then it checks if the newest one has
    been updated since saving it (using ETag). If there are any updates, it saves
    a new copy to the database.
    """
    repo = await db.scalar(
        select(Repository)
        .where(Repository.name == name)
        .where(Repository.owner == owner)
        .where(Repository.branch == branch)
        .order_by(Repository.creation_date.desc())
        .limit(1)
    )

    response = None

    endpoint = (
        f"https://api.github.com/repos/{owner}/{name}/git/trees/{branch}?recursive=true"
    )
    auth = None
    if settings.github_username and settings.github_token:
        auth = (settings.github_username, settings.github_token)
    async with httpx.AsyncClient(auth=auth) as client:
        if repo is None:
            response = await client.get(endpoint)
        else:
            response = await client.get(endpoint, headers={"If-None-Match": repo.etag})

    if response.status_code != status.HTTP_304_NOT_MODIFIED:
        repo = Repository(
            name=name,
            owner=owner,
            branch=branch,
            etag=response.headers["etag"],
            data=_parse_response(response),
        )
        db.add(repo)
        await db.commit()

    return repo.id


async def get_repo(*, db: AsyncSession, repo_id: int) -> Repository:
    """Returns the repository with given id or raises a 404 HTTPException if it does not exist."""
    repo = await db.scalar(select(Repository).where(Repository.id == int(repo_id)))
    if repo is None:
        raise HTTPException(status_code=404, detail="Repository not found")

    return repo


async def get_directory(
    *, db: AsyncSession, repo_id: int, directory_id: str
) -> Directory:
    """Returns the directory with given id that belongs to the repository.

    Raises a 404 HTTPException if the repository does not exist or it
    does not contain this directory.
    """
    await get_repo(db=db, repo_id=repo_id)

    val = literal_column("value", type_=JSONB)

    directory = await db.scalar(
        select(val)
        .select_from(Repository, func.jsonb_array_elements(Repository.data).alias())
        .where(Repository.id == int(repo_id))
        .where(val.contains({"sha": directory_id}))
    )

    if directory is None:
        raise HTTPException(status_code=404, detail="Directory not found")

    q = await db.scalars(
        select(val)
        .select_from(Repository, func.jsonb_array_elements(Repository.data).alias())
        .where(Repository.id == int(repo_id))
        .where(val.contains({"parent": directory["path"]}))
        .where(val.contains({"type": "tree"}))
    )
    subdirectories = q.all()

    return Directory(
        id=directory["sha"],
        name=directory["path"].split("/")[-1],
        subdirectories=[
            DirectoryInfo(id=subdir["sha"], name=subdir["path"].split("/")[-1])
            for subdir in subdirectories
        ],
    )


async def get_root_directory(*, db: AsyncSession, repo_id: int) -> Directory:
    """Returns the root directory of the repository with given id.

    Raises a 404 HTTPException if the repository does not exist.
    """
    await get_repo(db=db, repo_id=repo_id)

    val = literal_column("value", type_=JSONB)

    q = await db.scalars(
        select(val)
        .select_from(Repository, func.jsonb_array_elements(Repository.data).alias())
        .where(Repository.id == int(repo_id))
        .where(val.contains({"parent": ""}))
        .where(val.contains({"type": "tree"}))
    )

    subdirectories = q.all()

    return Directory(
        id="",
        name="",
        subdirectories=[
            DirectoryInfo(id=subdir["sha"], name=subdir["path"].split("/")[-1])
            for subdir in subdirectories
        ],
    )


async def get_random_file_path(*, db: AsyncSession, repo_id: int) -> str:
    """Returns path to a randomly selected file that belongs to the repository.

    Raises a 404 HTTPException if the repository does not exist.
    The returned path is in the format 'a/b/c/file.txt'.
    """
    await get_repo(db=db, repo_id=repo_id)

    val = literal_column("value", type_=JSONB)

    q = await db.scalars(
        select(val)
        .select_from(Repository, func.jsonb_array_elements(Repository.data).alias())
        .where(Repository.id == int(repo_id))
        .where(val.contains({"type": "blob"}))
    )

    return random.choice(q.all())["path"]


def _parse_response(response):
    data = response.json()["tree"]
    for item in data:
        item["parent"] = "/".join(item["path"].split("/")[:-1])
    return data
