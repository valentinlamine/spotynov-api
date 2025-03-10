import base64
import os

import requests
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from app.services.auth_service import AuthService


# Charger les variables d'environnement du fichier .env
load_dotenv()

# Récupérer les variables d'environnement
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Endpoint pour lier le compte Spotify
@router.get("/connect")
async def connect_spotify(token: str = Depends(oauth2_scheme)):
    # Vérifier la validité du token utilisateur via AuthService
    username, error_message = AuthService.verify_token(token)

    if username is None:
        raise HTTPException(status_code=401, detail=error_message)

    auth_url = (
        f"https://accounts.spotify.com/authorize?response_type=code&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}&scope=user-library-read user-read-private"
    )
    return {"auth_url": auth_url}


@router.get("/callback")
async def spotify_callback(code: str, token: str = Depends(oauth2_scheme)):
    """
    Récupère le token d'accès Spotify et lie le compte à l'utilisateur.
    """

    # Vérifier la validité du token utilisateur via AuthService
    username, error_message = AuthService.verify_token(token)
    if username is None:
        raise HTTPException(status_code=401, detail=error_message)

    # Créer un en-tête d'autorisation avec les identifiants de Spotify
    auth_header = {
        "Authorization": f"Basic {base64.b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode()).decode()}"
    }

    # Échanger le code d'autorisation contre un token d'accès
    response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "authorization_code",
            "code": code,  # Le code reçu de Spotify
            "redirect_uri": REDIRECT_URI,
        },
        headers=auth_header,
    )

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Erreur lors de la récupération du token Spotify")

    data = response.json()
    spotify_access_token = data["access_token"]

    # Utiliser l'API Spotify pour obtenir des informations sur l'utilisateur
    user_response = requests.get(
        "https://api.spotify.com/v1/me",
        headers={"Authorization": f"Bearer {spotify_access_token}"},
    )

    if user_response.status_code != 200:
        raise HTTPException(status_code=500, detail="Erreur lors de la récupération des informations Spotify")

    spotify_user_info = user_response.json()

    # Lier le compte Spotify avec l'utilisateur
    success, message = AuthService.link_spotify_account(username, spotify_user_info)
    if success:
        return {"message": "Compte Spotify lié avec succès"}
    else:
        raise HTTPException(status_code=400, detail=message)
