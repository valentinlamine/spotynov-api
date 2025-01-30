# app/services/spotify_service.py

class SpotifyService:
    def __init__(self):
        # Initialise tout ce qui est nécessaire pour l'intégration avec Spotify
        pass

    def link_account(self, user_id: str, spotify_token: str):
        """
        Lier le compte Spotify de l'utilisateur avec le service.
        """
        # Ajouter la logique pour lier l'utilisateur à son compte Spotify
        pass

    def get_current_playback(self, user_id: str):
        """
        Retourner le morceau en cours de lecture pour l'utilisateur.
        """
        # Cette méthode pourrait appeler l'API de Spotify pour récupérer la lecture actuelle
        return {"track": "A Sample Track", "artist": "Artist Name"}
