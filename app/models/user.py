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
    groupName: str = None
    spotifyToken: str = None
