from app.database import init_models
from fastapi import FastAPI
from app.routers import game

app = FastAPI()


app.include_router(game.router)


@app.on_event("startup")
async def on_startup():
    await init_models()


@app.get("/")
async def root():
    return {"message": "Hello World"}
