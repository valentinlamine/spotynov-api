from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles


from app.api.auth import router as auth_router
from app.api.groups import router as groups_router
from app.api.spotify import router as spotify_router
from app.front.front import router as front_router
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permet les origines spécifiées
    allow_credentials=True,
    allow_methods=["*"],  # Permet toutes les méthodes (GET, POST, etc.)
    allow_headers=["*"],  # Permet tous les en-têtes
)

app.include_router(auth_router, prefix="/api/auth")
app.include_router(groups_router, prefix="/api/groups")
app.include_router(spotify_router, prefix="/api/spotify")
app.include_router(front_router, prefix="")

app.mount("/assets", StaticFiles(directory="front/assets"), name="assets")
