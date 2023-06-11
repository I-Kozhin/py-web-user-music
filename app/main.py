from fastapi import FastAPI

from app.database.database import init_models
from app.routers.audio_router import audio_router
from app.routers.user_router import user_router
from app.settings import HOST, PORT

from app.errors import logger

app = FastAPI()
app.include_router(user_router)
app.include_router(audio_router)


@app.on_event("startup")
async def startup_event():
    try:
        await init_models()
    except Exception as e:
        logger.exception(f'Failed to perform {startup_event} func: {e}')
        raise  # exit


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST, port=PORT)
