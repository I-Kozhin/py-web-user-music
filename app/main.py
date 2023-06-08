from fastapi import FastAPI

from app.database.database import init_models
from app.routers.audio_router import audio_router
from app.routers.user_router import user_router

# HOST = '0.0.0.0'
HOST = 'localhost'
PORT = 8000

app = FastAPI()
app.include_router(user_router)
app.include_router(audio_router)


@app.on_event("startup")
async def startup_event():
    await init_models()


@app.get("/")
def root():
    return {"If you can see this message": "Then it is OK"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST, port=PORT)
