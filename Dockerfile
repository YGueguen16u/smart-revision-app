FROM python:3.8-slim

WORKDIR /app

# Copier les fichiers de dépendances
COPY requirements.txt .
COPY package.json .

# Créer et activer l'environnement virtuel
RUN python -m venv venv
ENV PATH="/app/venv/bin:$PATH"

# Installer les dépendances dans l'environnement virtuel
RUN . venv/bin/activate && pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y nodejs npm && npm install

# Copier le reste du code
COPY . .

# Créer les répertoires nécessaires
RUN mkdir -p data/config data/decks data/multimedia/images data/multimedia/audio data/multimedia/video

# Exposer le port
EXPOSE 8000

# Commande de démarrage avec l'environnement virtuel
CMD ["venv/bin/python", "app.py"]
