import json
from app.models.user import User
from app.models.group import Group


class JSONStorage:

    def __init__(self, filepath="users.json"):
        self.filepath = filepath
        self.data = self.load_data()

    def load_data(self):
        try:
            with open(self.filepath, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {"users": [], "groups": []}

    def save_data(self):
        with open(self.filepath, "w") as file:
            json.dump(self.data, file, indent=4)

    def save_user(self, user: User):
        self.data["users"].append(user.dict())
        self.save_data()
        return True

    def get_user_by_username(self, username: str):
        for user in self.data["users"]:
            if user["username"] == username:
                return User(**user)
        return None
