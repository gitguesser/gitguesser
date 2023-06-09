from json import dumps

import pytest

SAMPLE_REPOSITORY_DATA = [
    {
        "player_name": "player",
        "repo_owner": "gitguesser",
        "repo_name": "gitguesser",
        "repo_branch": "main",
    },
]


# We need test repo in our app. So we add one using game route.
async def create_repository(client, repo_data):
    response = await client.post("game/", content=dumps(repo_data))
    response = await client.get("game/" + str(response.json()["game_id"]))

    repo_id = response.json()["repository_id"]
    assert isinstance(repo_id, int)

    return repo_id


@pytest.mark.parametrize("repo_data", SAMPLE_REPOSITORY_DATA)
@pytest.mark.anyio
async def test_get_correct_repository(client, repo_data):
    repo_id = await create_repository(client, repo_data)
    response = await client.get("repository/" + str(repo_id))
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["id"] == repo_id
    assert response_json["name"] == repo_data["repo_name"]
    assert response_json["owner"] == repo_data["repo_owner"]
    assert response_json["branch"] == repo_data["repo_branch"]

    return repo_id


@pytest.mark.parametrize("repo_data", SAMPLE_REPOSITORY_DATA)
@pytest.mark.anyio
async def test_correct_repository_get_root_directory(client, repo_data):
    repo_id = await test_get_correct_repository(client, repo_data)
    response = await client.get("repository/" + str(repo_id) + "/tree")
    assert response.status_code == 200
    response_json = response.json()
    assert "subdirectories" in response_json
    assert any(dir["name"] == "backend" for dir in response_json["subdirectories"])
    assert any(dir["name"] == "frontend" for dir in response_json["subdirectories"])
    assert all(len(dir["id"]) > 0 for dir in response_json["subdirectories"])

    backend_dir_id = [
        dir["id"] for dir in response_json["subdirectories"] if dir["name"] == "backend"
    ][0]
    return str(repo_id) + "/tree/" + str(backend_dir_id)


@pytest.mark.parametrize("repo_data", SAMPLE_REPOSITORY_DATA)
@pytest.mark.anyio
async def test_correct_repository_get_no_directory(client, repo_data):
    repo_id = await test_get_correct_repository(client, repo_data)
    response = await client.get("repository/" + str(repo_id) + "/tree/0")
    assert response.status_code == 404
    assert response.json() == {"detail": "Directory not found"}


@pytest.mark.parametrize("repo_data", SAMPLE_REPOSITORY_DATA)
@pytest.mark.anyio
async def test_correct_repository_get_correct_directory(client, repo_data):
    directory_url = await test_correct_repository_get_root_directory(client, repo_data)
    response = await client.get("repository/" + directory_url)
    assert response.status_code == 200
    response_json = response.json()
    assert "subdirectories" in response_json
    assert any(dir["name"] == "app" for dir in response_json["subdirectories"])
    assert any(dir["name"] == "tests" for dir in response_json["subdirectories"])
    assert all(len(dir["id"]) > 0 for dir in response_json["subdirectories"])


@pytest.mark.anyio
async def test_get_no_repository(client):
    response = await client.get("repository/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Repository not found"}


@pytest.mark.anyio
async def test_no_repository_get_no_directory(client):
    response = await client.get("repository/1/tree/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Repository not found"}


@pytest.mark.anyio
async def test_no_repository_get_root_directory(client):
    response = await client.get("repository/1/tree")
    assert response.status_code == 404
    assert response.json() == {"detail": "Repository not found"}
