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
    token: str = None
    tokenExpiration: datetime = None
    groupName: str = None
    spotifyToken: str = None
    spotifyTokenExpiration: datetime = None
