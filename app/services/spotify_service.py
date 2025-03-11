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
        # Récupère les 10 derniers morceaux aimés par l'utilisateur
        headers = {"Authorization": f"Bearer {spotify_token}"}
        response = requests.get(f"https://api.spotify.com/v1/me/tracks?limit={limit}", headers=headers)

        if response.status_code != 200:
            raise Exception("Erreur lors de la récupération des morceaux aimés")

        return response.json()["items"]

    @staticmethod
    def analyze_tracks(spotify_token: str, track_ids: list) -> dict:

        if not track_ids:
            return {"error": "Aucun track ID fourni."}

        headers = {"Authorization": f"Bearer {spotify_token}"}
        audio_features = []
        batch_size = 100

        for i in range(0, len(track_ids), batch_size):
            batch_ids = ",".join(track_ids[i:i + batch_size])
            response = requests.get(f"{SpotifyService.SPOTIFY_API_URL}/audio-features?ids={batch_ids}",
                                    headers=headers)

            if response.status_code == 200:
                audio_features.extend(response.json().get("audio_features", []))

        if not audio_features:
            return {"error": "Impossible de récupérer les caractéristiques audio."}

        # Analyse des traits de personnalité
        traits = ["danceability", "energy", "valence"]
        personality_traits = {trait: sum(track[trait] for track in audio_features if track) / len(audio_features)
                              for trait in traits}

        return personality_traits

    @staticmethod
    def get_personality(spotify_token: str) -> dict:

        liked_tracks = SpotifyService.get_last_liked_songs(spotify_token)  
        if not liked_tracks:
            return {"error": "Aucun titre liké trouvé."}

        track_ids = [track["track"]["id"] for track in liked_tracks if "track" in track]
        return {"personality_traits": SpotifyService.analyze_tracks(spotify_token, track_ids)}






