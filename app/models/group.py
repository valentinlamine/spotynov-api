# app/models/group.py
from pydantic import BaseModel
from typing import List

class Group(BaseModel):
    name: str
    admin: str  # Identifiant de l'administrateur
    members: List[str]  # Liste des membres (identifiants des utilisateurs)
