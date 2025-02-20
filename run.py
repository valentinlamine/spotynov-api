from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from app.api.auth import router as auth_router
from app.api.groups import router as groups_router
from app.api.spotify import router as spotify_router
from app.front.front import router as front_router

app = FastAPI()

app.include_router(auth_router, prefix="/api/auth")
app.include_router(groups_router, prefix="/api/groups")
app.include_router(spotify_router, prefix="/api/spotify")
app.include_router(front_router, prefix="")

app.mount("/assets", StaticFiles(directory="front/assets"), name="assets")
