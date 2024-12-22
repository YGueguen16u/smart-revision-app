"""
Configuration des tests pour l'application.
"""
import pytest
import shutil
from pathlib import Path
import sys

# Ajoute le répertoire parent au PYTHONPATH
sys.path.append(str(Path(__file__).parent.parent))

from app import app

@pytest.fixture
def client():
    """Fixture fournissant un client de test Flask"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def clean_data_dir():
    """Fixture fournissant un répertoire de données propre pour les tests"""
    data_dir = Path(app.config['DATA_FOLDER'])
    decks_dir = Path(app.config['DECKS_FOLDER'])
    config_dir = Path(app.config['CONFIG_FOLDER'])
    
    # Crée les répertoires s'ils n'existent pas
    decks_dir.mkdir(parents=True, exist_ok=True)
    config_dir.mkdir(parents=True, exist_ok=True)
    
    # Supprime tous les fichiers existants
    for file in decks_dir.glob('*.json'):
        file.unlink()
    for file in config_dir.glob('*.json'):
        file.unlink()
        
    yield data_dir
    
    # Nettoyage après les tests
    for file in decks_dir.glob('*.json'):
        file.unlink()
    for file in config_dir.glob('*.json'):
        file.unlink()
