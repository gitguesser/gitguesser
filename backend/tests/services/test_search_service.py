import pytest
from app.services import search_service
from fastapi import HTTPException


@pytest.mark.anyio
async def test_search_repos():
    data = await search_service.search_repos(query="python")

    assert len(data.repos) > 0


@pytest.mark.anyio
async def test_search_incorrect():
    with pytest.raises(HTTPException) as excinfo:
        await search_service.search_repos(query="")
