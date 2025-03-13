from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from app.services.auth_service import AuthService
from app.models.user import SimplifiedUser

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/signup")
async def signup(user: SimplifiedUser):
    success, message = AuthService.create_user(user)
    if success:
        return {"message": message}
    else:
        raise HTTPException(status_code=400, detail=message)


@router.post("/login")
async def login(user: SimplifiedUser):
    token, message = AuthService.login(user)
    if token:
        return {"access_token": token, "detail": message}
    else:
        raise HTTPException(status_code=401, detail="Identifiants incorrects")


@router.get("/verify-token")
async def verify_token(token: str = Depends(oauth2_scheme)):
    """
    Vérifie la validité du token JWT et retourne les infos de l'utilisateur.
    """
    print("verify token : " + token)
    username, error_message = AuthService.verify_token(token)
    print(username, error_message)

    if username is None:
        print("no user")
        raise HTTPException(status_code=401, detail=error_message)
    return {"username": username, "message": error_message}