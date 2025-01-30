# app/api/users.py
from fastapi import APIRouter, HTTPException
from app.services.auth_service import AuthService
from app.models.user import User
from app.services.spotify_service import SpotifyService

router = APIRouter()


@router.post("/signup")
async def signup(user: User):
    if AuthService.create_user(user):
        return {"message": "Utilisateur créé avec succès"}
    else:
        raise HTTPException(status_code=400, detail="Erreur lors de la création de l'utilisateur")


@router.post("/login")
async def login(user: User):
    token = AuthService.login(user)
    if token:
        return {"token": token}
    else:
        raise HTTPException(status_code=401, detail="Identifiants incorrects")


@router.get("/me")
async def get_user_info(user: User):
    # Tu peux ajouter ici la logique pour obtenir les infos de l'utilisateur connecté
    return {"username": user.username, "spotify_linked": user.spotify_linked}
