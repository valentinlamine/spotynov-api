# app/services/group_service.py
from tokenize import group

from app.storage.group_storage import GroupStorage
from app.storage.user_storage import UserStorage
from app.models.group import Group
from app.models.user import User
import random


class GroupService:

    def __init__(self):
        self.__init__()

    @staticmethod
    def create_group(group_name: str, user_id: int):
        storage = GroupStorage()
        # Vérifie si le groupe existe déjà
        if storage.get_group_by_name(group_name) is not None:
            return False, f"Le groupe '{group_name}' existe déjà"

        new_group = Group(
            name=group_name,
            admin=user_id,
            members=[user_id]
        )

        storage.save_group(new_group)

        return True, f"Groupe '{group_name}' créé avec succès"

    @staticmethod
    def list_groups():
        storage = GroupStorage()

        storage.get_groups()

        groups_names = [group["name"] for group in storage.data["groups"]]

        return groups_names

    @staticmethod
    def add_user_to_group(user_id: int, group_name: str):
        storage_group = GroupStorage()
        storage_user = UserStorage()

        storage_group.get_group_by_name(group_name).members.append(user_id)
        storage_user.get_user_by_id(user_id).groupName = group_name

        storage_group.save_data()

        return

    @staticmethod
    def remove_user_from_group(user_id: int):
        storage_group = GroupStorage()
        group_name = storage_group.get_user_group_name(user_id)
        # vérifie si l'utilisateur est dans un groupe
        if group_name is None:
            return False
        # vérifie si l'utilisateur est l'admin du groupe
        if storage_group.is_user_admin(user_id, group_name):
            storage_group.set_random_admin(user_id, group_name)
        # vérifie si l'utilisateur est le seul membre du groupe
        members = storage_group.get_group_members(user_id)
        if len(members) == 1:
            storage_group.delete_group_by_name(group_name)
        else:
            storage_group.remove_user_from_group(user_id, group_name)
        return True

    @staticmethod
    def delete_group_by_name(name: str):
        storage = GroupStorage()
        initial_length = len(storage.data["group"])
        storage.data["group"] = [group for group in storage.data["group"] if group["name"] != name]

        if len(storage.data["group"]) < initial_length:
            storage.save_data()
            return True
        return False

    @staticmethod
    def get_group_members(user_id: int):
        storage_group = GroupStorage()
        return storage_group.get_group_members(user_id)



    @staticmethod
    def set_random_admin(group_name: str):
        storage = GroupStorage()

        grp = storage.get_group_by_name(group_name)

        rand = random.randint(0, grp.members.count() - 1)

        grp.admin = grp.members[rand]

        return

    @staticmethod
    def join_group(user_id: int, group_name: str):
        storage_group = GroupStorage()
        # check if group exists
        if storage_group.get_group_by_name(group_name) is None:
            return False, f"Le groupe '{group_name}' n'existe pas"
        user_group_name = storage_group.get_user_group_name(user_id)
        # vérifie si l'utilisateur est déjà dans le groupe
        if user_group_name == group_name:
            return False, f"Vous êtes déjà dans le groupe '{group_name}'"

        if storage_group.join_group(user_id, group_name):
            return True, f"Vous avez rejoint le groupe '{group_name}'"
        return False, f"Impossible de rejoindre le groupe '{group_name}'"

    @staticmethod
    def get_user_group_name(user_id: int):
        storage = GroupStorage()
        return storage.get_user_group_name(user_id)
