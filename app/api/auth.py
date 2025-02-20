from fastapi import APIRouter, HTTPException, Depends
from app.services.auth_service import AuthService
from app.models.user import SimplifiedUser

router = APIRouter()


@router.post("/signup")
async def signup(user: SimplifiedUser):
    success, message = AuthService.create_user(user)
    if success:
        return {"message": message}
    else:
        raise HTTPException(status_code=400, detail=message)


@router.post("/login")
async def login(user: SimplifiedUser):
    token = AuthService.login(user)
    if token:
        return {"token": token}
    else:
        raise HTTPException(status_code=401, detail="Identifiants incorrects")
