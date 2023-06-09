import pytest
from app.dependencies import get_session
from app.main import app
from httpx import AsyncClient


@pytest.fixture
async def client(db):
    app.dependency_overrides[get_session] = lambda: db
    async with AsyncClient(app=app, base_url="http://test/") as client:
        yield client
    app.dependency_overrides.clear()
