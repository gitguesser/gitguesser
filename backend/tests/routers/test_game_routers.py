from datetime import datetime
from json import dumps

import pytest
from pydantic.datetime_parse import parse_datetime

CORRECT_GAME_DATA = [
    {
        "player_name": "player",
        "repo_owner": "gitguesser",
        "repo_name": "gitguesser",
        "repo_branch": "main",
    },
]

INCORRECT_GAME_DATA = [
    {},
    {
        "repo_owner": "gitguesser",
        "repo_name": "gitguesser",
        "repo_branch": "main",
    },
    {
        "player_name": "player",
        "repo_owner": "I don't have this repo",
        "repo_name": "gitguesser",
        "repo_branch": "main",
    },
]


@pytest.mark.parametrize("game_data", INCORRECT_GAME_DATA)
@pytest.mark.anyio
async def test_post_incorrect_game(client, game_data):
    response = await client.post("game/", content=dumps(game_data))
    assert (
        response.status_code == 404 or response.status_code == 422
    )  # Maybe add json check but i don't think it is worth the effort.


@pytest.mark.parametrize("game_data", CORRECT_GAME_DATA)
@pytest.mark.anyio
async def test_post_correct_game(client, game_data):
    start_time = datetime.now()

    response = await client.post("game/", content=dumps(game_data))
    assert response.status_code == 200
    assert response.json()["game_id"] == 1

    new_game_data = response.json()
    new_game_data["start_time"] = start_time
    return new_game_data


@pytest.mark.parametrize("game_data", CORRECT_GAME_DATA)
@pytest.mark.anyio
async def test_get_correct_game(client, game_data):
    new_game_data = await test_post_correct_game(client, game_data)
    max_time = datetime.now()

    response = await client.get("game/" + str(new_game_data["game_id"]))
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["id"] == new_game_data["game_id"]
    assert response_json["player_name"] == game_data["player_name"]
    assert "repository_id" in response_json and isinstance(
        response_json["repository_id"], int
    )
    assert "start_time" in response_json
    start_time = parse_datetime(response_json["start_time"])
    assert new_game_data["start_time"] <= start_time <= max_time


@pytest.mark.parametrize("game_data", CORRECT_GAME_DATA)
@pytest.mark.anyio
async def test_correct_game_get_results_without_answer(client, game_data):
    new_game_data = await test_post_correct_game(client, game_data)

    response = await client.get("game/" + str(new_game_data["game_id"]) + "/results")
    assert response.status_code == 404
    assert response.json() == {"detail": "Game not found"}


@pytest.mark.parametrize("game_data", CORRECT_GAME_DATA)
@pytest.mark.anyio
async def test_correct_game_post_answer(client, game_data):
    new_game_data = await test_post_correct_game(client, game_data)

    sample_answer = {"answer": "sample"}
    new_game_data["answer"] = "sample"
    response = await client.post(
        "game/" + str(new_game_data["game_id"]), content=dumps(sample_answer)
    )
    assert response.status_code == 200

    return new_game_data


@pytest.mark.parametrize("game_data", CORRECT_GAME_DATA)
@pytest.mark.anyio
async def test_correct_game_get_results_with_answer(client, game_data):
    new_game_data = await test_correct_game_post_answer(client, game_data)

    response = await client.get("game/" + str(new_game_data["game_id"]) + "/results")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["player_answer"] == new_game_data["answer"]
    assert "end_time" in response_json
    assert "score" in response_json
    assert "player_answer" in response_json


@pytest.mark.anyio
async def test_get_no_game(client):
    response = await client.get("game/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Game not found"}


@pytest.mark.anyio
async def test_no_game_get_results(client):
    response = await client.get("game/1/results")
    assert response.status_code == 404
    assert response.json() == {"detail": "Game not found"}


@pytest.mark.anyio
async def test_no_game_post_answer(client):
    sample_answer = {"answer": "sample"}
    response = await client.post("game/1", content=dumps(sample_answer))
    assert response.status_code == 404
    assert response.json() == {"detail": "Game not found"}
