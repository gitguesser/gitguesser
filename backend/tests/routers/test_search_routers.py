import pytest


@pytest.mark.anyio
async def test_search(client):
    response = await client.get("search/?query=java")
    assert response.status_code == 200
    assert "repos" in response.json()
    assert len(response.json()["repos"]) > 0


@pytest.mark.anyio
async def test_search_incorrect(client):
    response = await client.get("search/")
    assert response.status_code == 404
