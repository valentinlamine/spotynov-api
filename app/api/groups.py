# app/api/groups.py
from fastapi import APIRouter, HTTPException
from app.models.group import Group, SimplifiedGroup
from app.services.group_service import GroupService

router = APIRouter()


@router.post("/create")
async def create_group(group: SimplifiedGroup):
    if GroupService.create_group(group.group_name, group.user_id):
        return {"message": f"Groupe '{group.group_name}' créé avec succès"}
    else:
        raise HTTPException(status_code=400, detail="Erreur lors de la création du groupe")


@router.get("/list")
async def list_groups():
    groups = GroupService.list_groups()
    return {"groups": groups}


@router.get("/members")
async def list_members(group: SimplifiedGroup):
    members = GroupService.get_group_members(group.user_id, group.group_name)
    if members:
        return {"members": members}
    else:
        raise HTTPException(status_code=404, detail="Groupe non trouvé")


@router.post("/remove_user_from_group")
async def remove_user_from_group(group: SimplifiedGroup):
    if GroupService.remove_user_from_group(group.user_id, group.group_name):
        return {"message": f"Groupe '{group.group_name}' créé avec succès"}
    else:
        raise HTTPException(status_code=400, detail="Erreur lors de la création du groupe")
