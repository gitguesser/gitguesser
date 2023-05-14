from fastapi import APIRouter
from schemas.game import GameInfo, GameResults, GameStartConfig, PlayerAnswer
import asyncpg

router = APIRouter(
    prefix="/game",
    tags=["game"],
)

async def save_game_to_database(game_id, player_name, repo_name, repo_owner, start_time):
    connection = await asyncpg.connect(
        host="db",
        user="gitguesser",
        password="gitguesser",
        database="gitguesser_db"
    )
    
    sql = "INSERT INTO games (game_id, player_name, repo_name, repo_owner, start_time) VALUES ($1, $2, $3, $4, $5)"
    values = (game_id, player_name, repo_name, repo_owner, start_time)

    await connection.execute(sql, *values)

    await connection.close()

@router.post(
    "/",
    response_model=GameInfo,
    description="Starts a new game.",
)
async def start_game(game_start_config: GameStartConfig):
    game_id = generate_game_id()
    start_time = datetime.now()
    
    player_name = game_start_config.player_name
    repo_name = game_start_config.repo_name
    repo_owner = game_start_config.repo_owner
    
    save_game_to_database(game_id, player_name, repo_name, repo_owner, start_time)


@router.get(
    "/{id}",
    response_model=GameInfo,
    description="Retrieves information about a game with given id.",
)
async def get_game_info(id: int):
    connection = await asyncpg.connect(
        host="db",
        user="gitguesser",
        password="gitguesser",
        database="gitguesser_db"
    )
    
    sql = "SELECT * FROM games WHERE id = $1"
    values = (id,)
    
    result = await connection.fetchrow(sql, *values)
    await connection.close()
    
    if result:
        game_info = GameInfo(
            game_id=result["id"],
            repo_id=result["repository_id"],
            player_name=result["player_name"],
            repo_name=result["repo_name"],
            repo_owner=result["repo_owner"],
            start_time=result["start_time"]
        )
        return game_info
    
    raise HTTPException(status_code=404, detail="Game not found")


@router.get(
    "/{id}/results",
    response_model=GameResults,
    description="Retrieves results of finished game with given id.",
)
async def get_game_results(id: int):
    connection = await asyncpg.connect(
        host="db",
        user="gitguesser",
        password="gitguesser",
        database="gitguesser_db"
    )
    
    sql = "SELECT * FROM games WHERE id = $1"
    values = (id,)
    
    result = await connection.fetchrow(sql, *values)
    await connection.close()
    
    if result:
        game_info = GameInfo(
            end_time: datetime,
            score: int,
            player_answer: str,
            correct_answer: str
        )
        return game_info
    
    raise HTTPException(status_code=404, detail="Game not found")


@router.post("/{id}", description="Sends player answer for a game with given id.")
async def send_answer(id: int, answer: PlayerAnswer):
    connection = await asyncpg.connect(
        host="db",
        user="gitguesser",
        password="gitguesser",
        database="gitguesser_db"
    )
    
    sql = "UPDATE games SET player_answer = $1 WHERE id = $2"
    values = (answer.answer, id)
    
    result = await connection.execute(sql, *values)
    await connection.close()
    
    if result == "UPDATE 1":
        return {"message": "Answer sent successfully"}
    
    raise HTTPException(status_code=404, detail="Game not found")
