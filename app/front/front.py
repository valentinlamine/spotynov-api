from fastapi import APIRouter
from fastapi.responses import FileResponse
import os

router = APIRouter()

# Page d'accueil
@router.get("/")
async def home():
    return FileResponse(os.path.join("front", 'register', 'register.html'))


# Page d'inscription (register)
@router.get("/register")
async def register():
    return FileResponse(os.path.join("front", 'register', 'register.html'))


# Page de connexion (login)
@router.get("/login")
async def login():
    return FileResponse(os.path.join("front", 'login', 'login.html'))


# Page d'accueil après connexion
@router.get("/home")
async def home_page():
    return FileResponse(os.path.join("front", 'home', 'home.html'))


@router.get("/callback")
async def callback():
    return FileResponse(os.path.join("front", "spotify", "callback.html"))
