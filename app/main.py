import asyncio

import typer
from fastapi import FastAPI

from app.database.database import init_models
from app.routers.user_router import user_router
from app.routers.audio_router import audio_router

# HOST = '0.0.0.0'
HOST = 'localhost'
PORT = 8000

app = FastAPI()
app.include_router(user_router)
app.include_router(audio_router)


@app.on_event("startup")
async def startup_event():
    await init_models()


if __name__ == "__main__":

    import uvicorn

    uvicorn.run(app, host=HOST, port=PORT)
