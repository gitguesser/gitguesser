from app.schemas.search import Repositories
from app.services import search_service
from fastapi import APIRouter

router = APIRouter(
    prefix="/search",
    tags=["search"],
)


@router.get(
    "/",
    response_model=Repositories,
    description="Gets repositories from GitHub.",
)
async def search_repos(query: str = ""):
    return await search_service.search_repos(query=query)
