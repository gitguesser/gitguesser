import httpx
from app.config import settings
from app.schemas.search import Repositories, Repository
from fastapi import HTTPException, status


async def search_repos(*, query: str) -> list[Repository]:
    """Finds repositories on Github."""
    endpoint = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page=100"
    auth = None
    if settings.github_username and settings.github_token:
        auth = (settings.github_username, settings.github_token)
    async with httpx.AsyncClient(auth=auth) as client:
        response = await client.get(endpoint)

    if response.status_code == status.HTTP_200_OK:
        data = response.json()["items"]
        return Repositories(
            repos=[
                Repository(
                    name=item["name"],
                    owner=item["owner"]["login"],
                    branch=item["default_branch"],
                )
                for item in data
            ]
        )
    raise HTTPException(status_code=404, detail="Error connecting to GitHub API")
