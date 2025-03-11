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

        new_group = Group(
            name=group_name,
            admin=user_id,
            members=[user_id]
        )

        storage.save_group(new_group)

        return True

    @staticmethod
    def list_groups():
        storage = GroupStorage()

        groups_names = []

        for i in range(storage.data.count()):
            groups_names.append(storage.data[i].name)

        return groups_names

    @staticmethod
    def add_user_to_group(user_id: int, group_name: str):
        storage_group = GroupStorage()
        storage_user = UserStorage()

        storage_group.get_group_by_name(group_name).members.append(user_id)
        storage_user.get_user_by_id(user_id).groupName = group_name

        storage_group.save_data()

        return

    def remove_user_from_group(self, user_id: int, group_name: str):
        storage_group = GroupStorage()
        storage_user = UserStorage()

        group = storage_group.get_group_by_name(group_name)

        group.members.remove(user_id)
        storage_user.get_user_by_id(user_id).groupName = ""

        if group.admin == user_id:
            group.admin = self.set_random_admin(group_name)

        if not group.members:
            self.delete_group_by_name(group_name)

        storage_group.save_data()

        return

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
    def get_group_members(user_id: int, group_name: str):
        storage_group = GroupStorage()
        if user_id in storage_group.get_group_by_name(group_name).members:
            return storage_group.get_group_by_name(group_name).members
        return []

    @staticmethod
    def set_random_admin(group_name: str):
        storage = GroupStorage()

        grp = storage.get_group_by_name(group_name)

        rand = random.randint(0, grp.members.count() - 1)

        grp.admin = grp.members[rand]

        return

    @staticmethod
    def join_group(self, user_id: int, group_name: str):
        storage_group = GroupStorage()
        storage_user = UserStorage()
        grp: any

        if storage_group.get_group_by_name(group_name) is None:
            self.create_group(group_name, user_id)
        else:
            grp = storage_group.get_group_by_name(group_name)


        if user_id in grp.members:
            return False

        grp.members.append(user_id)
        storage_user.get_user_by_id(user_id).groupName = group_name

        storage_group.save_data()

        return True



