# app/services/auth_service.py
import datetime
import os

import jwt
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from app.models.user import User, SimplifiedUser
from app.storage.user_storage import UserStorage

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


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
            return None, "Identifiants incorrects"

        # Génération du token JWT
        access_token = AuthService.create_access_token({"sub": user.username})
        return access_token, "Connexion réussie"

    @staticmethod
    def create_access_token(data: dict):
        """
        Génère un token JWT avec une date d'expiration.
        """
        to_encode = data.copy()
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})

        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def verify_token(token: str):
        """
        Vérifie si un token est valide.
        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                return None
            return username
        except jwt.ExpiredSignatureError:
            return None, "Token expiré"
