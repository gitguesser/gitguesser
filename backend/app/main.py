from config import settings
from database import init_models
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import game

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.frontend_url,
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(game.router)


@app.on_event("startup")
async def on_startup():
    await init_models()


@app.get("/")
async def root():
    return {"message": "Hello World"}
