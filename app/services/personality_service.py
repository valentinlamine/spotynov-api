import requests

class SpotifyAnalyzer:
    SPOTIFY_API_URL = "https://api.spotify.com/v1"

    @staticmethod
    def get_liked_tracks(spotify_token: str, limit: int = 50) -> list:

        # Récupère tous les titres likés de l'utilisateur en gérant la pagination.

        headers = {"Authorization": f"Bearer {spotify_token}"}
        liked_tracks = []
        url = f"{SpotifyAnalyzer.SPOTIFY_API_URL}/me/tracks?limit={limit}"

        while url:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                return []

            data = response.json()
            liked_tracks.extend(data.get("items", []))
            url = data.get("next")  # Récupère l'URL de la page suivante

        return liked_tracks





