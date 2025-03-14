# Utilisation de Python 3.11 léger
FROM python:3.11-slim

# Définition du dossier de travail
WORKDIR /app

# Copier les fichiers de dépendances et installer les packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du projet
COPY . .

# Exposer le port (valeur par défaut 8000)
EXPOSE 8000

# Définir les variables d'environnement avec des valeurs par défaut (modifiables via Docker)
ARG CLIENT_ID=""
ARG CLIENT_SECRET=""
ARG REDIRECT_URI=""
ARG SECRET_KEY=""
ARG HOST="0.0.0.0"
ARG PORT="8000"

ENV CLIENT_ID=$CLIENT_ID
ENV CLIENT_SECRET=$CLIENT_SECRET
ENV REDIRECT_URI=$REDIRECT_URI
ENV SECRET_KEY=$SECRET_KEY
ENV HOST=$HOST
ENV PORT=$PORT

# Lancer l'application avec Uvicorn
CMD ["sh", "-c", "uvicorn run:app --host $HOST --port $PORT"]
