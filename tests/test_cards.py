import pytest
import json
from pathlib import Path
import sys

# Ajoute le répertoire parent au PYTHONPATH
sys.path.append(str(Path(__file__).parent.parent))

from app import app
from .test_deck import test_create_deck, test_view_deck_page

@pytest.mark.dependency(depends=["tests.test_deck::test_create_deck", "tests.test_deck::test_view_deck_page"])
def test_add_card_to_deck(client, clean_data_dir):
    """Test l'ajout d'une carte à un deck"""
    # Crée un deck
    response = client.post('/api/decks', json={'name': 'Test Deck'})
    assert response.status_code == 201
    deck = response.get_json()
    
    # Ajoute une carte
    card_data = {
        'question': 'Quelle est la capitale de la France ?',
        'answer': 'Paris'
    }
    response = client.post(f'/api/decks/{deck["id"]}/cards', json=card_data)
    assert response.status_code == 201
    
    # Vérifie que la carte a été ajoutée
    response = client.get(f'/api/decks/{deck["id"]}')
    assert response.status_code == 200
    deck_data = response.get_json()
    assert len(deck_data['flashcards']) == 1
    assert deck_data['flashcards'][0]['question'] == card_data['question']
    assert deck_data['flashcards'][0]['answer'] == card_data['answer']

@pytest.mark.dependency(depends=["tests.test_cards::test_add_card_to_deck"])
def test_edit_card(client, clean_data_dir):
    """Test la modification d'une carte"""
    # Crée un deck avec une carte
    response = client.post('/api/decks', json={'name': 'Test Deck'})
    deck = response.get_json()
    
    card_data = {
        'question': 'Question originale',
        'answer': 'Réponse originale'
    }
    response = client.post(f'/api/decks/{deck["id"]}/cards', json=card_data)
    card = response.get_json()
    
    # Modifie la carte
    updated_data = {
        'question': 'Question modifiée',
        'answer': 'Réponse modifiée'
    }
    response = client.put(f'/api/decks/{deck["id"]}/cards/{card["id"]}', json=updated_data)
    assert response.status_code == 200
    
    # Vérifie que la carte a été modifiée
    response = client.get(f'/api/decks/{deck["id"]}')
    deck_data = response.get_json()
    assert deck_data['flashcards'][0]['question'] == updated_data['question']
    assert deck_data['flashcards'][0]['answer'] == updated_data['answer']

@pytest.mark.dependency(depends=["tests.test_cards::test_add_card_to_deck"])
def test_review_card(client, clean_data_dir):
    """Test la révision d'une carte"""
    # Crée un deck avec une carte
    response = client.post('/api/decks', json={'name': 'Test Deck'})
    deck = response.get_json()
    
    card_data = {
        'question': 'Question test',
        'answer': 'Réponse test'
    }
    response = client.post(f'/api/decks/{deck["id"]}/cards', json=card_data)
    assert response.status_code == 201
    
    # Vérifie que la carte peut être révisée
    card = response.get_json()
    response = client.get(f'/api/decks/{deck["id"]}/cards/{card["id"]}')
    assert response.status_code == 200
    card_data = response.get_json()
    assert 'question' in card_data
    assert 'answer' in card_data
