from app.database import init_models
from app.routers import game, repository, search
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(game.router)
app.include_router(repository.router)
app.include_router(search.router)


@app.on_event("startup")
async def on_startup():
    await init_models()


@app.get("/")
async def root():
    return {"message": "Hello World"}
