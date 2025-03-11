from fastapi import APIRouter, Depends, HTTPException
from app.api.auth import verify_token  # Import de la vérification du token

router = APIRouter()


@router.get("/home")
async def home(username: str = Depends(verify_token)):
    if username is None:
        raise HTTPException(status_code=401, detail="Accès non autorisé")
    return {"message": f"Bienvenue {username} sur la page home !"}