from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from app.models.spotify import SpotifyTokenRequest
from app.models.user import LikedSongClass
from app.services.spotify_service import SpotifyService
from app.services.auth_service import AuthService
from app.storage.user_storage import UserStorage

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/connect")
async def connect_spotify(token: str = Depends(oauth2_scheme)):
    # Vérifier la validité du token utilisateur via AuthService
    username, error_message = AuthService.verify_token(token)

    if username is None:
        raise HTTPException(status_code=401, detail=error_message)

    # Récupérer l'URL d'autorisation depuis le service Spotify
    auth_url = SpotifyService.get_authorization_url()

    return {"auth_url": auth_url}


# Endpoint pour récupérer le token Spotify
@router.get("/callback")
async def spotify_callback(code: str):
    try:
        # Échanger le code d'autorisation contre un token d'accès
        access_token = SpotifyService.exchange_code_for_token(code)

        return {"access_token": access_token}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/link")
async def spotify_link(
        spotify_token_request: SpotifyTokenRequest,  # Le token Spotify dans le body
        token: str = Depends(oauth2_scheme),  # Le token de l'utilisateur (Bearer token)
):
    # Vérifier la validité du token utilisateur via AuthService
    username, error_message = AuthService.verify_token(token)

    if username is None:
        raise HTTPException(status_code=401, detail=error_message)

    # Récupérer le token Spotify envoyé dans le body de la requête
    spotify_token = spotify_token_request.spotify_token

    try:
        # Enregistrer le token Spotify pour cet utilisateur
        AuthService.set_spotify_token(username, spotify_token)

        return {"message": "Le compte Spotify a été lié avec succès."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint pour récupérer le morceau en cours de lecture pour l'utilisateur
@router.get("/current-playback")
async def current_playback(token: str = Depends(oauth2_scheme)):
    # Vérifier la validité du token utilisateur via AuthService
    username, error_message = AuthService.verify_token(token)

    if username is None:
        raise HTTPException(status_code=401, detail=error_message)

    try:
        # Utiliser le token Spotify pour récupérer le morceau en cours de lecture
        spotify_token = AuthService.get_spotify_token(username)
        if spotify_token is None:
            raise HTTPException(status_code=401, detail="Erreur lors de la récupération du token Spotify")

        playback = SpotifyService.get_current_playback(spotify_token)

        return {"track": playback}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get-last-liked-songs")
async def get_last_liked_songs(
        username: LikedSongClass,
        token: str = Depends(oauth2_scheme)):
    # Vérifier la validité du token utilisateur via AuthService
    username.username, error_message = AuthService.verify_token(token)

    if username.username is None:
        raise HTTPException(status_code=401, detail=error_message)

    try:
        # Utiliser le token Spotify pour récupérer les derniers morceaux aimés
        spotify_token = AuthService.get_spotify_token(username.username)
        if spotify_token is None:
            raise HTTPException(status_code=401, detail="Erreur lors de la récupération du token Spotify")

        liked_songs = SpotifyService.get_last_liked_songs(spotify_token, username.limit)

        # Stocke les morceaux like dans la base de donnée de l'utilisateur
        storage = UserStorage()
        storage.set_liked_playlist(username.username, liked_songs)

        return {"liked_songs": liked_songs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analyze-tracks")
async def analyze_tracks(token: str = Depends(oauth2_scheme)):
    # Vérifier la validité du token utilisateur via AuthService
    username, error_message = AuthService.verify_token(token)

    if username is None:
        raise HTTPException(status_code=401, detail=error_message)

    try:
        # Utiliser le token Spotify pour récupérer les morceaux aimés
        spotify_token = AuthService.get_spotify_token(username)
        if spotify_token is None:
            raise HTTPException(status_code=401, detail="Erreur lors de la récupération du token Spotify")

        personality = SpotifyService.get_personality(spotify_token)

        return personality
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
