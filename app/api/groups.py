# app/api/groups.py
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from app.models.group import GroupName
from app.services.auth_service import AuthService
from app.services.group_service import GroupService

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/create")
async def create_group(
        name: GroupName,
        token: str = Depends(oauth2_scheme)):
    # Vérifier la validité du token utilisateur via AuthService
    username, error_message = AuthService.verify_token(token)

    if username is None:
        raise HTTPException(status_code=401, detail=error_message)

    user_id = AuthService.get_user_id(username)
    user_group = GroupService.get_user_group_name(user_id)

    success, message = GroupService.create_group(name.name, user_id)

    if success:
        # Supprimer le groupe de l'utilisateur s'il en a déjà un
        if user_group:
            GroupService.remove_user_from_group(user_id)
        return {"message": message}
    else:
        raise HTTPException(status_code=400, detail=message)


@router.get("/list")
async def list_groups(token: str = Depends(oauth2_scheme)):
    # Vérifier la validité du token utilisateur via AuthService
    username, error_message = AuthService.verify_token(token)

    if username is None:
        raise HTTPException(status_code=401, detail=error_message)

    groups = GroupService.list_groups()
    return {"groups": groups}


@router.get("/members")
async def list_members(token: str = Depends(oauth2_scheme)):
    # Vérifier la validité du token utilisateur via AuthService
    username, error_message = AuthService.verify_token(token)

    if username is None:
        raise HTTPException(status_code=401, detail=error_message)

    user_id = AuthService.get_user_id(username)

    members = GroupService.get_group_members(user_id)
    if members:
        # transformer les ids en noms d'utilisateur
        members = [AuthService.get_username_by_id(member) for member in members]
        return {"members": members}
    else:
        raise HTTPException(status_code=404, detail="Groupe non trouvé")


@router.post("/leave")
async def remove_user_from_group(token: str = Depends(oauth2_scheme)):
    # Vérifier la validité du token utilisateur via AuthService
    username, error_message = AuthService.verify_token(token)

    if username is None:
        raise HTTPException(status_code=401, detail=error_message)

    user_id = AuthService.get_user_id(username)

    if GroupService.remove_user_from_group(user_id):
        return {"message": "Vous avez quitté le groupe"}
    else:
        raise HTTPException(status_code=400, detail="Impossible de quitter le groupe")


@router.post("/join")
async def join_group(
        name: GroupName,
        token: str = Depends(oauth2_scheme)):
    # Vérifier la validité du token utilisateur via AuthService
    username, error_message = AuthService.verify_token(token)

    if username is None:
        raise HTTPException(status_code=401, detail=error_message)

    user_id = AuthService.get_user_id(username)

    group_name = GroupService.get_user_group_name(user_id)
    if group_name == name.name:
        raise HTTPException(status_code=400, detail="Vous êtes déjà dans ce groupe")

    if group_name:
        GroupService.remove_user_from_group(user_id)

    success, message = GroupService.join_group(user_id, name.name)

    if success:
        return {"message": message}
    else:
        raise HTTPException(status_code=400, detail=message)


@router.post("/get-group")
async def get_group(token: str = Depends(oauth2_scheme)):
    # Vérifier la validité du token utilisateur via AuthService
    username, error_message = AuthService.verify_token(token)

    if username is None:
        raise HTTPException(status_code=401, detail=error_message)

    user_id = AuthService.get_user_id(username)

    group_name = GroupService.get_user_group_name(user_id)
    if group_name:
        return {"group": group_name}
    else:
        raise HTTPException(status_code=404, detail="Groupe non trouvé")


@router.get("/get-admin")
async def get_group_admin(token: str = Depends(oauth2_scheme)):
    # Vérifier la validité du token utilisateur via AuthService
    username, error_message = AuthService.verify_token(token)

    if username is None:
        raise HTTPException(status_code=401, detail=error_message)

    user_id = AuthService.get_user_id(username)

    admin_id = GroupService.get_group_admin(user_id)
    if admin_id:
        admin = AuthService.get_username_by_id(admin_id)
        return {"admin": admin}
    else:
        raise HTTPException(status_code=404, detail="Groupe non trouvé")