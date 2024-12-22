"""
Test Flows - Scénarios de test complets avec création d'un deck de mathématiques
"""
import pytest
from datetime import datetime, timedelta
import json
from pathlib import Path
import sys

# Ajouter le répertoire parent au PYTHONPATH
sys.path.append(str(Path(__file__).parent.parent))

from app import (
    get_all_decks,
    get_deck,
    create_deck,
    add_card,
    update_card,
    get_difficulty_settings,
    update_difficulty_settings
)

@pytest.mark.flow
class TestApplicationFlow:
    """
    Scénario complet : Création et utilisation d'un deck de mathématiques
    """
    
    @pytest.mark.dependency()
    def test_flow_1_base_application(self, client, clean_data_dir):
        """[T1] Configuration initiale de l'application"""
        # T1.1 Vérification de la page d'accueil
        response = client.get('/')
        assert response.status_code == 200
        
        # T1.2 Configuration des paramètres de difficulté
        difficulty_settings = {
            'very_hard': 1,  # 1 heure
            'hard': 6,      # 6 heures
            'medium': 24,   # 1 jour
            'easy': 72,     # 3 jours
            'very_easy': 168 # 1 semaine
        }
        
        # Utilisation directe de la fonction de app.py
        with app.test_request_context():
            app.config['CONFIG_FOLDER'] = str(clean_data_dir)
            update_difficulty_settings(difficulty_settings)
            current_settings = get_difficulty_settings()
            assert current_settings == difficulty_settings

    @pytest.mark.dependency(depends=["TestApplicationFlow::test_flow_1_base_application"])
    def test_flow_2_creation_deck_maths(self, client, clean_data_dir):
        """[T2] Création du deck de mathématiques"""
        with app.test_request_context():
            app.config['DECKS_FOLDER'] = str(clean_data_dir)
            
            # T2.1 Création du deck principal
            deck_data = {
                'name': 'Mathématiques',
                'description': 'Révisions de mathématiques niveau terminale',
                'flashcards': []
            }
            deck = create_deck(deck_data)
            assert deck['deck_name'] == 'Mathématiques'
            
            # T2.2 Création des sous-sections
            sections = ['Algèbre', 'Analyse', 'Géométrie', 'Probabilités']
            section_decks = {}
            for section in sections:
                section_data = {
                    'name': f'Maths - {section}',
                    'description': f'Section {section} des mathématiques',
                    'flashcards': []
                }
                section_deck = create_deck(section_data)
                section_decks[section] = section_deck
                
            return deck, section_decks

    @pytest.mark.dependency(depends=["TestApplicationFlow::test_flow_2_creation_deck_maths"])
    def test_flow_3_ajout_cartes(self, client, clean_data_dir):
        """[T3] Ajout de différents types de cartes"""
        with app.test_request_context():
            app.config['DECKS_FOLDER'] = str(clean_data_dir)
            main_deck, section_decks = self.test_flow_2_creation_deck_maths(client, clean_data_dir)
            
            # T3.1 Cartes basiques
            cards_data = [
                {
                    'deck_id': section_decks['Algèbre']['id'],
                    'question': 'Qu\'est-ce qu\'un polynôme du second degré ?',
                    'answer': 'Une expression de la forme ax² + bx + c où a ≠ 0',
                    'type': 'basic'
                },
                {
                    'deck_id': section_decks['Analyse']['id'],
                    'question': 'Définition de la dérivée',
                    'answer': 'Limite du taux de variation en un point',
                    'type': 'basic'
                }
            ]
            
            # Ajout des cartes en utilisant la fonction de app.py
            for card_data in cards_data:
                deck_id = card_data.pop('deck_id')
                add_card(deck_id, card_data)
                
                # Vérification
                deck = get_deck(deck_id)
                assert len(deck['flashcards']) > 0
                latest_card = deck['flashcards'][-1]
                assert latest_card['question'] == card_data['question']

    @pytest.mark.dependency(depends=["TestApplicationFlow::test_flow_3_ajout_cartes"])
    def test_flow_4_session_revision(self, client, clean_data_dir):
        """[T4] Session de révision (à implémenter)"""
        pass

    @pytest.mark.dependency(depends=["TestApplicationFlow::test_flow_4_session_revision"])
    def test_flow_5_analyse_progression(self, client, clean_data_dir):
        """[T5] Analyse des résultats (à implémenter)"""
        pass

    @pytest.mark.dependency(depends=["TestApplicationFlow::test_flow_5_analyse_progression"])
    def test_flow_6_performance_long_terme(self, client, clean_data_dir):
        """[T6] Tests de performance sur la durée (à implémenter)"""
        pass
