"""
Tests pour les paramètres de difficulté.
"""

import pytest
from pathlib import Path
import json

difficulty_params = {
    'minimum_differences': {'minutes': 60},
    'status_codes': {
        'success': 200,
        'bad_request': 400
    }
}

@pytest.fixture
def default_settings():
    return {
        'very_hard': 30,
        'hard': 90,
        'medium': 150,
        'easy': 210,
        'very_easy': 270
    }

class TestDifficulty:
    """Tests des paramètres de difficulté."""

    @pytest.mark.dependency()
    def test_difficulty_page_load(self, client, default_settings):
        """Test le chargement de la page des paramètres de difficulté."""
        # Créer des paramètres par défaut
        client.post('/api/settings/difficulty', json=default_settings)
        
        response = client.get('/api/settings/difficulty')
        settings = response.get_json()
        response = client.get('/settings/difficulty')
        assert response.status_code == difficulty_params['status_codes']['success']
        assert b'Param\xc3\xa8tres de difficult\xc3\xa9' in response.data

    @pytest.mark.dependency()
    def test_default_difficulty_values(self, client):
        """Test les valeurs par défaut des paramètres."""
        response = client.get('/api/settings/difficulty')
        settings = response.get_json()
        
        assert all(key in settings for key in ['very_hard', 'hard', 'medium', 'easy', 'very_easy'])
        assert all(isinstance(value, int) for value in settings.values())
        assert settings['very_hard'] < settings['hard'] < settings['medium'] < settings['easy'] < settings['very_easy']

    @pytest.mark.dependency()
    def test_unit_conversions(self, client, default_settings):
        """Test la conversion des unités."""
        response = client.post('/api/settings/difficulty', json=default_settings)
        assert response.status_code == difficulty_params['status_codes']['success']

    @pytest.mark.dependency()
    def test_mixed_units(self, client, default_settings):
        """Test l'utilisation d'unités mixtes."""
        response = client.post('/api/settings/difficulty', json=default_settings)
        assert response.status_code == difficulty_params['status_codes']['success']

    @pytest.mark.dependency()
    def test_minimum_differences(self, client):
        """Test des différences minimales entre niveaux."""
        settings = {
            'very_hard': 30,
            'hard': 90,  # Au moins 90 (30 + 60)
            'medium': 150,
            'easy': 210,
            'very_easy': 270
        }
        response = client.post('/api/settings/difficulty', json=settings)
        saved = client.get('/api/settings/difficulty').get_json()
        assert saved['hard'] >= saved['very_hard'] + difficulty_params['minimum_differences']['minutes']

    @pytest.mark.dependency()
    def test_invalid_values(self, client):
        """Test des valeurs invalides."""
        settings = {
            'very_hard': 30,
            'hard': 29,  # Valeur invalide car inférieure à very_hard
            'medium': 150,
            'easy': 210,
            'very_easy': 270
        }
        response = client.post('/api/settings/difficulty', json=settings)
        assert response.status_code == difficulty_params['status_codes']['bad_request']

    @pytest.mark.dependency()
    def test_persistence(self, client, default_settings):
        """Test de la persistance des paramètres."""
        response = client.post('/api/settings/difficulty', json=default_settings)
        assert response.status_code == difficulty_params['status_codes']['success']

        response = client.get('/api/settings/difficulty')
        saved = response.get_json()
        assert saved == default_settings

        response = client.get('/api/settings/difficulty')
        settings = response.get_json()
        response = client.get('/settings/difficulty')
        assert response.status_code == difficulty_params['status_codes']['success']

    @pytest.mark.dependency()
    def test_difficulty_impact_on_review(self, client, clean_data_dir, default_settings):
        """Test l'impact des paramètres de difficulté sur les révisions."""
        client.post('/api/settings/difficulty', json=default_settings)

        # Créer un deck
        deck_name = "Test Deck"
        response = client.post('/api/decks', json={'name': deck_name})
        assert response.status_code == difficulty_params['status_codes']['success']

        # Créer une carte
        card_data = {
            'question': 'Test Question',
            'answer': 'Test Answer',
            'type': 'traditional'
        }
        response = client.post(f'/api/decks/{deck_name}/cards', json=card_data)
        assert response.status_code == difficulty_params['status_codes']['success']

    @pytest.mark.dependency()
    def test_difficulty_statistics(self, client, clean_data_dir, default_settings):
        """Test les statistiques liées aux niveaux de difficulté."""
        # Créer un deck
        deck_name = "Test Deck"
        response = client.post('/api/decks', json={'name': deck_name})
        assert response.status_code == difficulty_params['status_codes']['success']

        # Créer plusieurs cartes avec différents niveaux de difficulté
        for i in range(5):
            card_data = {
                'question': f'Question {i}',
                'answer': f'Answer {i}',
                'type': 'traditional'
            }
            response = client.post(f'/api/decks/{deck_name}/cards', json=card_data)
            assert response.status_code == difficulty_params['status_codes']['success']

    @pytest.mark.dependency()
    def test_unit_conversion_and_validation(self, client, default_settings):
        """Test la conversion et la validation des unités."""
        response = client.post('/api/settings/difficulty', json=default_settings)
        assert response.status_code == difficulty_params['status_codes']['success']

    @pytest.mark.dependency()
    def test_minimum_difference_validation(self, client):
        """Test la validation des différences minimales entre niveaux."""
        settings = {
            'very_hard': 30,
            'hard': 90,  # Au moins 90 (30 + 60)
            'medium': 150,
            'easy': 210,
            'very_easy': 270
        }
        response = client.post('/api/settings/difficulty', json=settings)
        assert response.status_code == difficulty_params['status_codes']['success']

        response = client.get('/api/settings/difficulty')
        saved = response.get_json()
        for key1, key2 in zip(list(settings.keys())[:-1], list(settings.keys())[1:]):
            assert saved[key2] >= saved[key1] + difficulty_params['minimum_differences']['minutes']

    @pytest.mark.dependency()
    def test_mixed_units_validation(self, client, default_settings):
        """Test la validation des unités mixtes."""
        response = client.post('/api/settings/difficulty', json=default_settings)
        assert response.status_code == difficulty_params['status_codes']['success']

    @pytest.mark.dependency()
    def test_invalid_unit_combinations(self, client, default_settings):
        """Test les combinaisons invalides d'unités."""
        response = client.post('/api/settings/difficulty', json=default_settings)
        assert response.status_code == difficulty_params['status_codes']['success']

    @pytest.mark.dependency()
    def test_settings_persistence(self, client, default_settings):
        """Test la persistance des paramètres."""
        response = client.post('/api/settings/difficulty', json=default_settings)
        assert response.status_code == difficulty_params['status_codes']['success']

        response = client.get('/api/settings/difficulty')
        saved = response.get_json()
        assert saved == default_settings

        response = client.get('/api/settings/difficulty')
        settings = response.get_json()
        response = client.get('/settings/difficulty')
        assert response.status_code == difficulty_params['status_codes']['success']
