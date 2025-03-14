# app/models/user.py
from datetime import datetime

from pydantic import BaseModel


class SimplifiedUser(BaseModel):
    username: str
    password: str


class User(BaseModel):
    id: int
    username: str
    password: str
    spotifyToken: str = None
    likedPlaylist: list = []


class LikedSongClass(BaseModel):
    username: str = None
    limit: int = 10


class UserNameClass(BaseModel):
    user: str
