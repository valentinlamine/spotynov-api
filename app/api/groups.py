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
    print(user_group)

    success, message = GroupService.create_group(name.name, user_id)

    if success:
        # Supprimer le groupe de l'utilisateur s'il en a déjà un
        if user_group:
            GroupService.remove_user_from_group(user_id, user_group)
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

    members = GroupService.get_group_members(username)
    if members:
        return {"members": members}
    else:
        raise HTTPException(status_code=404, detail="Groupe non trouvé")

"""
@router.post("/remove_user_from_group")
async def remove_user_from_group(token: str = Depends(oauth2_scheme)):
    if GroupService.remove_user_from_group(group.user_id, group.group_name):
        return {"message": f"Groupe '{group.group_name}' créé avec succès"}
    else:
        raise HTTPException(status_code=400, detail="Erreur lors de la création du groupe")


@router.post("/join_group")
async def join_group(token: str = Depends(oauth2_scheme)):
    if GroupService.join_group(group.user_id, group.group_name):
        return {"message": f"Vous avez rejoint le groupe '{group.group_name}'"}
    else:
        raise HTTPException(status_code=400, detail="Impossible de rejoindre le groupe")
"""