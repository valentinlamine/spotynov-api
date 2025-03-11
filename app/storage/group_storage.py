import json
import random

from app.models.group import Group

"""
{
    "groups": [
        {
            "name": "Groupe 1",
            "admin": 1,
            "members": [1, 2, 3]
        },
        {
            "name": "Groupe 2",
            "admin": 2,
            "members": [2, 3]
        },
        {
            "name": "Groupe 3",
            "admin": 3,
            "members": [1, 3]
        }
    ]
}
"""

class GroupStorage:

    def __init__(self, filepath="app/json/groups.json"):
        self.filepath = filepath
        self.data = self.load_data()

    def load_data(self):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
                # Vérifier si les données ont une clé "groups", sinon l'initialiser
                if "groups" not in data:
                    data["groups"] = []
                return data
        except (FileNotFoundError, json.JSONDecodeError):  # Gestion d'erreur si le fichier est introuvable ou mal formé
            return {"groups": []}  # Retourne un dictionnaire avec une clé "groups" vide

    def save_data(self):
        with open(self.filepath, "w") as file:
            json.dump(self.data, file, indent=4)

    def save_group(self, group: Group):
        self.data["groups"].append(group.dict())
        self.save_data()
        return True

    def get_group_by_name(self, name: str):
        for group in self.data["groups"]:
            if group["name"] == name:
                return group
        return None

    def get_user_group_name(self, user_id: int):
        for group in self.data["groups"]:
            if user_id in group["members"]:
                return group["name"]
        return None

    def remove_user_from_group(self, user_id, group_name):
        for group in self.data["groups"]:
            if group["name"] == group_name:
                group["members"].remove(user_id)
                self.save_data()
                return True
        return False

    def get_group_members(self, user_id, group_name):
        # return the list of members of the group
        for group in self.data["groups"]:
            if group["name"] == group_name:
                return group["members"]

    def delete_group_by_name(self, group_name):
        initial_length = len(self.data["groups"])
        self.data["groups"] = [group for group in self.data["groups"] if group["name"] != group_name]

        if len(self.data["groups"]) < initial_length:
            self.save_data()
            return True
        return False

    def is_user_admin(self, user_id, group_name):
        for group in self.data["groups"]:
            if group["name"] == group_name:
                return group["admin"] == user_id
        return False

    def set_random_admin(self, user_id, group_name):
        # Parcours de tous les groupes
        for group in self.data["groups"]:
            if group["name"] == group_name:
                members = group["members"]

                # Retirer l'admin actuel du tirage au sort
                members_without_current_admin = [member for member in members if member != user_id]

                if len(members_without_current_admin) == 0:
                    # Si tous les membres sont déjà l'administrateur actuel, on ne peut pas tirer au sort
                    return False

                # Tirage aléatoire d'un membre
                new_admin = random.choice(members_without_current_admin)

                # Mise à jour de l'administrateur
                group["admin"] = new_admin
                self.save_data()
                return True
        return False

    def get_group_members(self, user_id, group_name):
        for group in self.data["groups"]:
            if group["name"] == group_name:
                return group["members"]
        return []

    def get_groups(self):
        return self.data["groups"]