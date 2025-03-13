from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from app.models.spotify import SpotifyTokenRequest
from app.models.user import LikedSongClass, UserNameClass
from app.services.group_service import GroupService
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
async def analyze_tracks(
        user: UserNameClass,
        token: str = Depends(oauth2_scheme)):
    # Vérifier la validité du token utilisateur via AuthService
    username, error_message = AuthService.verify_token(token)

    if username is None:
        raise HTTPException(status_code=401, detail=error_message)

    # vérifier si l'utilisateur existe
    if AuthService.get_user_id(user.user) is None:
        raise HTTPException(status_code=401, detail="Utilisateur non trouvé")

    try:
        # Utiliser le token Spotify pour récupérer les morceaux aimés
        spotify_token = AuthService.get_spotify_token(user.user)
        if spotify_token is None:
            raise HTTPException(status_code=401, detail="Erreur lors de la récupération du token Spotify")

        personality = SpotifyService.get_personality(spotify_token)

        return personality
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/create-playlist-from-likes")
async def create_playlist_from_likes(
        user: UserNameClass,  # Utilisateur cible pour récupérer les morceaux likés
        token: str = Depends(oauth2_scheme)):
    # Vérifier la validité du token utilisateur via AuthService
    connected_user_username, error_message = AuthService.verify_token(token)

    if connected_user_username is None:
        raise HTTPException(status_code=401, detail=error_message)

    if AuthService.get_user_id(user.user) is None:
        raise HTTPException(status_code=401, detail="Utilisateur cible non trouvé")

    try:
        # Récupérer le token Spotify de l'utilisateur connecté
        user_spotify_token = AuthService.get_spotify_token(connected_user_username)
        if user_spotify_token is None:
            raise HTTPException(status_code=401, detail="Erreur lors de la récupération du token Spotify")

        # Récupérer le token Spotify de l'utilisateur cible (l'autre utilisateur)
        target_spotify_token = AuthService.get_spotify_token(user.user)
        if target_spotify_token is None:
            raise HTTPException(status_code=401, detail="Erreur lors de la récupération du token Spotify de l'utilisateur cible")

        # Récupérer les 10 derniers morceaux aimés de l'utilisateur cible
        liked_songs = SpotifyService.get_last_liked_songs(target_spotify_token, limit=10)

        if not liked_songs:
            raise HTTPException(status_code=404, detail="Aucun titre liké trouvé pour cet utilisateur.")

        # Créer une playlist pour l'utilisateur connecté
        playlist_name = f"Playlist des 10 derniers morceaux likés de {user.user}"
        playlist_id = SpotifyService.create_playlist(user_spotify_token, playlist_name)

        # Ajouter les morceaux à la playlist créée
        track_ids = [song["track"]["id"] for song in liked_songs]
        SpotifyService.add_tracks_to_playlist(user_spotify_token, playlist_id, track_ids)

        return {"message": "Playlist créée avec succès", "playlist_id": playlist_id, "tracks_added": len(track_ids)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/synchronize")
async def synchronize_playback(
        token: str = Depends(oauth2_scheme)):
    # Vérifier la validité du token utilisateur via AuthService
    admin_username, error_message = AuthService.verify_token(token)

    if admin_username is None:
        raise HTTPException(status_code=401, detail=error_message)

    # vérifier si l'utilisateur est dans un groupe
    user_id = AuthService.get_user_id(admin_username)
    user_group_name = GroupService.get_user_group_name(user_id)
    if not user_group_name:
        raise HTTPException(status_code=401, detail="Vous n'êtes dans aucun groupe.")

    # vérifier si l'utilisateur est l'administrateur du groupe
    if not GroupService.is_user_admin(user_id, user_group_name):
        raise HTTPException(status_code=401, detail="Vous n'êtes pas l'administrateur du groupe.")

    # Récupérer tous les utilisateurs du groupe
    group_users_id = GroupService.get_group_members(user_id)
    if not group_users_id:
        raise HTTPException(status_code=404, detail="Aucun membre trouvé dans le groupe.")

    # Récupérer le token Spotify de l'administrateur pour savoir ce qu'il est en train d'écouter
    admin_spotify_token = AuthService.get_spotify_token(admin_username)
    if not admin_spotify_token:
        raise HTTPException(status_code=401,
                            detail="Erreur lors de la récupération du token Spotify de l'administrateur")

    try:
        # Récupérer les informations de la lecture en cours de l'administrateur
        playback = SpotifyService.get_current_playback(admin_spotify_token)

        # Synchroniser la musique sur tous les appareils des membres du groupe
        for user_id in group_users_id:
            # récupérer le nom des utilisateurs
            user = AuthService.get_username_by_id(user_id)
            if user == admin_username:
                continue
            # Récupérer le token Spotify de chaque membre
            user_spotify_token = AuthService.get_spotify_token(user)
            if user_spotify_token:
                # Démarrer la lecture sur l'appareil actif du membre à la même position que l'administrateur
                SpotifyService.start_playback(user_spotify_token, playback['item']['id'], playback['progress_ms'])

            else:
                print(f"Le membre {user} n'a pas de token Spotify enregistré.")

        return {"message": "La musique a été synchronisée sur tous les appareils des membres du groupe."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
