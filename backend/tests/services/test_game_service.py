import pytest
from app.models.models import Game
from app.schemas.game import GameStartConfig
from app.services import game_service
from fastapi import HTTPException
from sqlalchemy import func, select

CORRECT_GAME_START_CONFIG = [
    GameStartConfig(
        player_name="player",
        repo_name="gitguesser",
        repo_owner="gitguesser",
        repo_branch="main",
    ),
]

INCORRECT_GAME_START_CONFIG = [
    GameStartConfig(
        player_name="player",
        repo_name="gitguesser",
        repo_owner="abcd",
        repo_branch="main",
    ),
    GameStartConfig(
        player_name="player",
        repo_name="gitguesser",
        repo_owner="gitguesser",
        repo_branch="master",
    ),
]


@pytest.fixture
async def game_id(db):
    return await game_service.start_game(
        db=db, game_config=CORRECT_GAME_START_CONFIG[0]
    )


async def _count(db):
    return await db.scalar(select(func.count("*")).select_from(Game))


@pytest.mark.parametrize("game_config", CORRECT_GAME_START_CONFIG)
@pytest.mark.anyio
async def test_start_game_correct(db, game_config):
    assert await _count(db) == 0

    id = await game_service.start_game(db=db, game_config=game_config)
    game = await db.scalar(select(Game).where(Game.id == int(id)))

    assert await _count(db) == 1
    assert game is not None
    assert game.player_name == game_config.player_name
    assert game.repository_id is not None


@pytest.mark.parametrize("game_config", INCORRECT_GAME_START_CONFIG)
@pytest.mark.anyio
async def test_start_game_incorrect(db, game_config):
    with pytest.raises(HTTPException) as excinfo:
        await game_service.start_game(db=db, game_config=game_config)

    assert excinfo.value.status_code == 404
    assert await _count(db) == 0


@pytest.mark.anyio
async def test_get_game_when_exists(db, game_id):
    game = await game_service.get_game(db=db, game_id=game_id)

    assert game is not None
    assert game.id == game_id


@pytest.mark.anyio
async def test_get_game_when_not_exists(db):
    with pytest.raises(HTTPException) as excinfo:
        await game_service.get_game(db=db, game_id=0)

    assert excinfo.value.status_code == 404
    assert await _count(db) == 0


@pytest.mark.anyio
async def test_give_answer_correct(db, game_id):
    game = await game_service.get_game(db=db, game_id=game_id)
    assert game.end_time is None
    assert game.player_answer is None

    answer = game.correct_answer
    await game_service.give_answer(db=db, game_id=game_id, answer=answer)

    game = await game_service.get_game(db=db, game_id=game_id)
    assert game.score == 0
    assert game.end_time is not None
    assert game.player_answer == answer


@pytest.mark.anyio
async def test_give_wrong_correct(db, game_id):
    game = await game_service.get_game(db=db, game_id=game_id)
    assert game.end_time is None
    assert game.player_answer is None

    answer = game.correct_answer + "/does_not_exist"
    await game_service.give_answer(db=db, game_id=game_id, answer=answer)

    game = await game_service.get_game(db=db, game_id=game_id)
    assert game.score > 0
    assert game.end_time is not None
    assert game.player_answer == answer
