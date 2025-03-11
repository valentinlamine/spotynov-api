# app/models/group.py
from pydantic import BaseModel
from typing import List


class Group(BaseModel):
    name: str
    admin: int  # Identifiant de l'administrateur
    members: List[int]  # Liste des membres (identifiants des utilisateurs)


class GroupName(BaseModel):
    name: str
