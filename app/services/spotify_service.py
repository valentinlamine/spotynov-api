# app/services/spotify_service.py
# Charger les variables d'environnement
import base64
import os

import requests
from dotenv import load_dotenv


load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")


class SpotifyService:
    def __init__(self):
        # Initialise tout ce qui est nécessaire pour l'intégration avec Spotify
        pass

    @staticmethod
    def get_authorization_url():
        scopes = (
            "user-library-read user-read-private user-read-email "
            "playlist-read-private playlist-modify-public playlist-modify-private "
            "user-top-read user-follow-read user-follow-modify "
            "user-read-playback-state user-read-currently-playing "
            "app-remote-control streaming"
        )

        auth_url = (
            f"https://accounts.spotify.com/authorize?response_type=code"
            f"&client_id={CLIENT_ID}"
            f"&redirect_uri={REDIRECT_URI}"
            f"&scope={scopes}"
        )
        return auth_url

    @staticmethod
    def exchange_code_for_token(code: str):
        """
        Échange le code d'autorisation contre un token d'accès.
        """
        auth_header = {
            "Authorization": f"Basic {base64.b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode()).decode()}"
        }

        response = requests.post(
            "https://accounts.spotify.com/api/token",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": REDIRECT_URI,
            },
            headers=auth_header,
        )

        if response.status_code != 200:
            raise Exception("Erreur lors de la récupération du token Spotify")

        data = response.json()
        access_token = data.get("access_token")

        if not access_token:
            raise Exception("Le token d'accès Spotify est manquant")

        return access_token

    @staticmethod
    def get_current_playback(spotify_token: str):
        """
        Retourne le morceau en cours de lecture pour l'utilisateur.
        """
        headers = {"Authorization": f"Bearer {spotify_token}"}
        response = requests.get("https://api.spotify.com/v1/me/player/currently-playing", headers=headers)

        if response.status_code == 204:
            return None

        if response.status_code != 200:
            raise Exception("Erreur lors de la récupération du morceau en cours de lecture")

        return response.json()

    @staticmethod
    def get_last_liked_songs(spotify_token, limit=10):
        """
        Récupère les morceaux aimés de l'utilisateur, avec gestion de la pagination.
        Si `limit` est défini à 0, récupère tous les morceaux aimés.
        """
        headers = {"Authorization": f"Bearer {spotify_token}"}
        liked_songs = []
        url = f"https://api.spotify.com/v1/me/tracks?limit={limit if limit > 0 else 50}"  # Limite de 50 morceaux par page

        while url:
            # Si on a une limite et qu'on avons déjà récupéré suffisamment de morceaux, on s'arrête
            if limit > 0 and len(liked_songs) >= limit:
                break

            response = requests.get(url, headers=headers)

            if response.status_code != 200:
                raise Exception("Erreur lors de la récupération des morceaux aimés")

            data = response.json()
            liked_songs.extend(data["items"])  # Ajouter les morceaux récupérés à la liste

            # Si la limite est définie à 0, on continue à récupérer la pagination jusqu'à ce qu'il n'y ait plus de pages
            if limit == 0:
                url = data.get("next")
            else:
                break  # Arrêter la récupération dès que le nombre de morceaux atteint la limite

        # Si la limite est définie à 0 et que la pagination est finie, on renvoie la liste complète
        return liked_songs[:limit] if limit > 0 else liked_songs

    @staticmethod
    def get_personality(spotify_token: str) -> dict:
        """
        Analyse les morceaux aimés de l'utilisateur pour déterminer sa personnalité,
        et calcule la popularité et la durée moyennes de ses morceaux préférés.
        """
        # Récupérer tous les morceaux aimés de l'utilisateur
        liked_tracks = SpotifyService.get_last_liked_songs(spotify_token)

        if not liked_tracks:
            return {"error": "Aucun titre liké trouvé."}

        # Récupérer les IDs des morceaux pour l'analyse de personnalité
        track_ids = [track["track"]["id"] for track in liked_tracks if "track" in track]

        # Calculer la popularité et la durée moyennes
        total_popularity = 0
        total_duration_ms = 0
        num_songs = len(liked_tracks)

        for track in liked_tracks:
            total_popularity += track["track"]["popularity"]
            total_duration_ms += track["track"]["duration_ms"]

        # Calculs de la popularité moyenne et de la durée moyenne
        average_popularity = total_popularity / num_songs
        average_duration_ms = total_duration_ms / num_songs

        # Convertir la durée moyenne en secondes
        average_duration_seconds = average_duration_ms / 1000

        # Retourner les résultats
        return {
            "average_popularity": average_popularity,
            "average_duration_seconds": average_duration_seconds
        }

    @staticmethod
    def create_playlist(user_spotify_token, playlist_name):
        headers = {"Authorization": f"Bearer {user_spotify_token}"}
        user_id = SpotifyService.get_spotify_user_id(user_spotify_token)

        if not user_id:
            raise Exception("Impossible de récupérer l'ID de l'utilisateur Spotify")

        response = requests.post(
            f"https://api.spotify.com/v1/users/{user_id}/playlists",
            headers=headers,
            json={"name": playlist_name, "public": False},
        )

        if response.status_code != 201:
            raise Exception("Erreur lors de la création de la playlist")

        return response.json()["id"]

    @staticmethod
    def get_spotify_user_id(user_spotify_token):
        headers = {"Authorization": f"Bearer {user_spotify_token}"}
        response = requests.get("https://api.spotify.com/v1/me", headers=headers)

        if response.status_code != 200:
            raise Exception("Impossible de récupérer l'ID de l'utilisateur Spotify")

        return response.json()["id"]

    @staticmethod
    def add_tracks_to_playlist(user_spotify_token, playlist_id, track_ids):
        headers = {"Authorization": f"Bearer {user_spotify_token}"}
        response = requests.post(
            f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks",
            headers=headers,
            json={"uris": [f"spotify:track:{track_id}" for track_id in track_ids]},
        )

        if response.status_code != 201:
            raise Exception("Erreur lors de l'ajout des morceaux à la playlist")

        return response.json()

    @classmethod
    def start_playback(cls, user_spotify_token, track_id, playback_ms=0):
        headers = {"Authorization": f"Bearer {user_spotify_token}"}

        # Corps de la requête avec seulement track_id et position_ms
        body = {
            "uris": [f"spotify:track:{track_id}"],
            "position_ms": playback_ms
        }

        # Faire la requête PUT pour démarrer la lecture
        response = requests.put(
            "https://api.spotify.com/v1/me/player/play",
            headers=headers,
            json=body
        )

        # Vérification du statut de la réponse
        if response.status_code == 204:
            # Lecture démarrée avec succès
            return {"success": True}
        elif response.status_code == 401:
            raise Exception("Non autorisé : Vérifiez votre token Spotify")
        elif response.status_code == 403:
            raise Exception("Accès refusé : L'API n'a pas permis d'effectuer cette action")
        elif response.status_code == 429:
            raise Exception("Trop de requêtes envoyées. Veuillez réessayer plus tard.")
        else:
            raise Exception(f"Erreur {response.status_code} : {response.text}")



