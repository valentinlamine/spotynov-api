from fastapi import APIRouter, HTTPException, Depends
from app.services.auth_service import AuthService
from app.models.user import User

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
