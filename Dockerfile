FROM python:3.8-slim

WORKDIR /app

# Copier les fichiers de dépendances
COPY requirements.txt .
COPY package.json .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y nodejs npm && npm install

# Copier le reste du code
COPY . .

# Créer les répertoires nécessaires
RUN mkdir -p data/config data/decks data/multimedia/images data/multimedia/audio data/multimedia/video

# Exposer le port
EXPOSE 8000

# Commande de démarrage
CMD ["python", "app.py"]
