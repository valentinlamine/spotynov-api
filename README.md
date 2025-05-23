# Projet FastAPI - Gestion des Groupes
## Membres du groupe
- Mattéo VOCANSON
- Valentin LAMINE
- Flavio NUNES
- Mathis GREDT
- Dimitri BRANCOURT

## Description
Ce projet est une API développée avec **FastAPI** permettant de gérer des groupes et leurs membres. Il inclut des fonctionnalités d'authentification, de gestion des groupes et d'intégration avec Spotify.

## Fonctionnalités
- Authentification avec JWT
- Gestion des groupes (création, récupération, administration)
- Liste des membres d'un groupe
- Intégration avec Spotify (récupération de playlists, etc.)
- Interface front simple pour la gestion des membres

## Prérequis
- **Docker** et **Docker Compose** installés
- **Python 3.11** (si exécution locale)

## Installation
### 1. Cloner le dépôt
```sh
git clone https://github.com/valentinlamine/spotynov-api
cd spotynov-api
```

### 2. Configuration des variables d'environnement
Créer un fichier `.env` à la racine avec le contenu suivant :
```env
CLIENT_ID=your_spotify_client_id
CLIENT_SECRET=your_spotify_client_secret
REDIRECT_URI=http://localhost:8000/api/spotify/callback
SECRET_KEY=your_secret_key
```
#### CLIENT_ID et CLIENT_SECRET sont trouvables sur le dashboard spotify developer.
#### REDIRECT_URI est l'adresse de redirection après l'authentification spotify.
#### SECRET_KEY est la clé de chiffrage pour les mots de passe.

### 3. Exécution avec Docker
#### Build de l'image Docker
```sh
docker build -t fastapi-app .
```

#### Lancer le conteneur
```sh
docker run --env-file .env -p 8000:8000 fastapi-app
```

### 4. Accéder à l'API
Le swagger de l'API est accessible à l'adresse suivante :
```
http://localhost:8000/docs
```

### 5. Utilisation de l'interface Front
Une interface utilisateur simple permet d'afficher la liste des membres et leurs détails.

## Développement et tests
### Exécution locale (hors Docker)
#### Installation des dépendances
```sh
pip install -r requirements.txt
```

#### Lancer l'application
```sh
python run.py
```


