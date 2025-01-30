# app/services/group_service.py
from app.storage.json_storage import JSONStorage
from app.models.group import Group
from app.models.user import User
import random


class GroupService:

    @staticmethod
    def create_group(group_name: str, user_id: str):
        # Créer un groupe et l'ajouter à la liste des groupes dans le storage
        storage = JSONStorage()
        group = Group(name=group_name, admin=user_id, members=[user_id])
        return storage.save_group(group)

    @staticmethod
    def list_groups():
        storage = JSONStorage()
        return storage.get_all_groups()

    @staticmethod
    def list_group_members(group_name: str):
        storage = JSONStorage()
        group = storage.get_group_by_name(group_name)
        if group:
            return group.members
        return None
