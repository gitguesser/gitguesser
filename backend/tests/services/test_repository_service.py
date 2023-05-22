import pytest
from fastapi import HTTPException
from sqlalchemy import func, select

from app.services import repository_service
from app.models.models import Repository


CORRECT_REPOSITORY = [
    {
        "owner": "gitguesser",
        "name": "gitguesser",
        "branch": "main",
    },
]

INCORRECT_REPOSITORY = [
    {
        "owner": "gitguesser",
        "name": "gitguesser",
        "branch": "master",
    },
    {
        "owner": "gitguesser",
        "name": "gitguesser1",
        "branch": "main",
    },
]


@pytest.fixture
async def repo_id(db):
    return await repository_service.update_repo(
        db=db, owner="gitguesser", name="gitguesser", branch="main"
    )


async def _count(db):
    return await db.scalar(select(func.count("*")).select_from(Repository))


@pytest.mark.parametrize("repo_data", CORRECT_REPOSITORY)
@pytest.mark.anyio
async def test_update_repo_correct(db, repo_data):
    assert await _count(db) == 0

    id = await repository_service.update_repo(db=db, **repo_data)
    repo = await db.scalar(select(Repository).where(Repository.id == int(id)))

    assert await _count(db) == 1
    assert repo is not None
    assert repo.name == repo_data["name"]
    assert repo.owner == repo_data["owner"]
    assert repo.branch == repo_data["branch"]
    assert len(repo.data) > 0


@pytest.mark.parametrize("repo_data", CORRECT_REPOSITORY)
@pytest.mark.anyio
async def test_update_repo_unchanged(db, repo_data):
    assert await _count(db) == 0

    await repository_service.update_repo(db=db, **repo_data)
    await repository_service.update_repo(db=db, **repo_data)

    assert await _count(db) == 1


@pytest.mark.parametrize("repo_data", INCORRECT_REPOSITORY)
@pytest.mark.anyio
async def test_update_repo_incorrect(db, repo_data):
    assert await _count(db) == 0

    with pytest.raises(HTTPException) as excinfo:
        await repository_service.update_repo(db=db, **repo_data)

    assert excinfo.value.status_code == 404
    assert await _count(db) == 0


@pytest.mark.anyio
async def test_get_repo_when_exists(db, repo_id):
    repo = await repository_service.get_repo(db=db, repo_id=repo_id)

    assert repo is not None
    assert repo.id == repo_id


@pytest.mark.anyio
async def test_get_repo_when_not_exists(db):
    with pytest.raises(HTTPException) as excinfo:
        repo = await repository_service.get_repo(db=db, repo_id=0)

    assert excinfo.value.status_code == 404
    assert await _count(db) == 0


@pytest.mark.anyio
async def test_get_directory_when_not_exists(db, repo_id):
    with pytest.raises(HTTPException) as excinfo:
        await repository_service.get_directory(db=db, repo_id=repo_id, directory_id="0")

    assert excinfo.value.status_code == 404


@pytest.mark.anyio
async def test_get_root_directory(db, repo_id):
    dir = await repository_service.get_root_directory(db=db, repo_id=repo_id)

    assert dir is not None
    assert dir.name == ""
    assert len(dir.subdirectories) > 0
    assert any(d.name == "backend" for d in dir.subdirectories)
    assert any(d.name == "frontend" for d in dir.subdirectories)
    assert all(len(d.id) > 0 for d in dir.subdirectories)


@pytest.mark.anyio
async def test_get_random_file_path(db, repo_id):
    path = await repository_service.get_random_file_path(db=db, repo_id=repo_id)

    assert path is not None


@pytest.mark.anyio
async def test_get_random_file_path_when_not_exists(db):
    with pytest.raises(HTTPException) as excinfo:
        await repository_service.get_random_file_path(db=db, repo_id=0)

    assert excinfo.value.status_code == 404
