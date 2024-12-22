"""
Tests pour les routes principales de l'application.
"""
import pytest
from app import app

@pytest.mark.dependency()
def test_home_page(client):
    """Test l'affichage de la page d'accueil"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Mes Decks de R\xc3\xa9vision' in response.data
    assert b'Cr\xc3\xa9er un nouveau deck' in response.data
    assert b'Param\xc3\xa8tres' in response.data

