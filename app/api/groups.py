# app/api/groups.py
from fastapi import APIRouter, HTTPException
from app.models.group import Group
from app.services.group_service import GroupService

router = APIRouter()


@router.post("/create")
async def create_group(group_name: str, user_id: str):
    if GroupService.create_group(group_name, user_id):
        return {"message": f"Groupe '{group_name}' créé avec succès"}
    else:
        raise HTTPException(status_code=400, detail="Erreur lors de la création du groupe")


@router.get("/list")
async def list_groups():
    groups = GroupService.list_groups()
    return {"groups": groups}


@router.get("/members/{group_name}")
async def list_members(group_name: str):
    members = GroupService.list_group_members(group_name)
    if members:
        return {"members": members}
    else:
        raise HTTPException(status_code=404, detail="Groupe non trouvé")
