from fastapi import APIRouter, HTTPException, Depends
from app.services.spotify_service import SpotifyService

router = APIRouter()


