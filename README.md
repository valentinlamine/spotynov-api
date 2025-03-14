# Projet FastAPI - Gestion des Groupes

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
git clone https://github.com/votre-repo.git
cd votre-repo
```

### 2. Configuration des variables d'environnement
Créer un fichier `.env` à la racine avec le contenu suivant :
```env
CLIENT_ID=your_spotify_client_id
CLIENT_SECRET=your_spotify_client_secret
REDIRECT_URI=http://localhost:8000/callback
SECRET_KEY=your_secret_key
HOST=0.0.0.0
PORT=8000
```

### 3. Exécution avec Docker
#### Build de l'image Docker
```sh
docker build --build-arg CLIENT_ID="your_client_id" \
             --build-arg CLIENT_SECRET="your_client_secret" \
             --build-arg REDIRECT_URI="http://localhost:8000/callback" \
             --build-arg SECRET_KEY="your_secret_key" \
             --build-arg HOST="0.0.0.0" \
             --build-arg PORT="8000" \
             -t fastapi-app .
```

#### Lancer le conteneur
```sh
docker run --env-file .env -p 8000:8000 fastapi-app
```

### 4. Accéder à l'API
L'API est accessible sur :
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

#### Lancer l'API
```sh
uvicorn run:app --host 0.0.0.0 --port 8000
```

### Tests
```sh
pytest tests/
```

## Contribuer
Les contributions sont les bienvenues ! Merci de créer une *issue* ou une *pull request*.

## Licence
Ce projet est sous licence MIT.

