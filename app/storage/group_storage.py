import json
from app.models.group import Group


class GroupStorage:

    def __init__(self, filepath="../json/groups.json"):
        self.filepath = filepath
        self.data = self.load_data()

    def load_data(self):
        try:
            with open(self.filepath, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_data(self):
        with open(self.filepath, "w") as file:
            json.dump(self.data, file, indent=4)

    def save_group(self, group: Group):
        self.data["group"].append(group.dict())
        self.save_data()
        return True

    def get_group_by_name(self, name: str):
        for group in self.data["group"]:
            if group["name"] == name:
                return group
        return None



