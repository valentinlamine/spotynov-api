# app/services/auth_service.py
import jwt
import datetime
import os
from passlib.context import CryptContext
from app.storage.user_storage import UserStorage
from app.models.user import User, SimplifiedUser
from dotenv import load_dotenv
import time

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


class AuthService:

    @staticmethod
    def create_user(user: SimplifiedUser):
        storage = UserStorage()

        # Hachage du mot de passe
        hashed_password = pwd_context.hash(user.password)

        # Conversion de SimplifiedUser en User (ajout d'id, valeur par défaut pour les autres champs)
        user = User(
            id=storage.get_last_user_id() + 1,
            username=user.username,
            password=hashed_password,
        )

        # Vérification de l'unicité du nom d'utilisateur
        if storage.get_user_by_name(user.username):
            return False, "Nom d'utilisateur déjà pris"

        # Stockage dans le fichier JSON
        if storage.save_user(user):
            return True, "Utilisateur créé avec succès"
        return False, "Erreur lors de la création de l'utilisateur"

    @staticmethod
    def login(user: SimplifiedUser):
        # Vérification des identifiants
        storage = UserStorage()
        stored_user = storage.get_user_by_name(user.username)

        if not stored_user:
            return None, "L'utilisateur n'existe pas"

        if not pwd_context.verify(user.password, stored_user["password"]):
            return None, "Identifiants incorrect"

        if stored_user and stored_user['password'] == pwd_context.hash(user.password):
            # Générer un token JWT ou une valeur aléatoire pour simuler un token
            return "fake-jwt-token"
        return None
