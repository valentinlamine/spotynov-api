import json
from app.models.user import User


class UserStorage:

    def __init__(self, filepath="app/json/users.json"):
        self.filepath = filepath
        self.data = self.load_data()

    def load_data(self):
        try:
            with open(self.filepath, "r") as file:
                data = json.load(file)
                # Vérifie que le fichier contient bien un dictionnaire
                if not isinstance(data, dict):
                    return {"users": [], "lastUserId": 0}
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            # Si le fichier est introuvable ou mal formé, retourne une structure vide correcte
            return {"users": [], "lastUserId": 0}

    def save_data(self):
        with open(self.filepath, "w",encoding="utf-8") as file:
            json.dump(self.data, file, indent=4, ensure_ascii=False)

    def save_user(self, user: User):
        self.data["users"].append(user.dict())
        self.data["lastUserId"] += 1
        self.save_data()
        return True

    def get_last_user_id(self):
        return self.data["lastUserId"]

    def get_user_by_name(self, name: str):
        for user in self.data["users"]:
            if user["username"] == name:
                return user
        return None

    def get_user_by_id(self, id: int):
        for user in self.data["users"]:
            if user["id"] == id:
                return user
        return None

    def delete_user_by_name(self, name: str):
        initial_length = len(self.data["user"])
        self.data["user"] = [user for user in self.data["user"] if user["name"] != name]

        if len(self.data["user"]) < initial_length:
            self.save_data()
            return True
        return False

    def delete_user_by_id(self, id: int):
        initial_length = len(self.data["user"])
        self.data["user"] = [user for user in self.data["user"] if user["id"] != id]

        if len(self.data["user"]) < initial_length:
            self.save_data()
            return True
        return False

    def set_spotify_token(self, username: str, spotify_token: str):
        for user in self.data["users"]:
            if user["username"] == username:
                user["spotifyToken"] = spotify_token
                self.save_data()
                return True
        return False
