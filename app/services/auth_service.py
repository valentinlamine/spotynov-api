# app/services/auth_service.py
import hashlib
from app.storage.json_storage import JSONStorage
from app.models.user import User
import time


class AuthService:

    @staticmethod
    def create_user(user: User):
        # Hachage du mot de passe
        user.password = hashlib.sha256(user.password.encode()).hexdigest()

        # Stockage dans le fichier JSON
        storage = JSONStorage()
        if storage.save_user(user):
            return True
        return False

    @staticmethod
    def login(user: User):
        # Vérification des identifiants
        storage = JSONStorage()
        stored_user = storage.get_user_by_username(user.username)
        if stored_user and stored_user.password == hashlib.sha256(user.password.encode()).hexdigest():
            # Générer un token JWT ou une valeur aléatoire pour simuler un token
            return "fake-jwt-token"
        return None
