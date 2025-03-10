from pydantic import BaseModel


class SpotifyTokenRequest(BaseModel):
    spotify_token: str
