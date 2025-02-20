# app/models/group.py
from pydantic import BaseModel
from typing import List


class SimplifiedGroup(BaseModel):
    user_id: int
    group_name: str


class Group(BaseModel):
    name: str
    admin: int  # Identifiant de l'administrateur
    members: List[int]  # Liste des membres (identifiants des utilisateurs)
