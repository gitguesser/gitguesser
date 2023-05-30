from app.database import init_models
from app.routers import game, repository
from fastapi import FastAPI

app = FastAPI()

app.include_router(game.router)
app.include_router(repository.router)

@app.on_event("startup")
async def on_startup():
    await init_models()


@app.get("/")
async def root():
    return {"message": "Hello World"}
