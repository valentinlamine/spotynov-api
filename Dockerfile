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

# Lancer l'application avec Uvicorn
CMD ["sh", "-c", "uvicorn run:app --host localhost --port 8000"]
