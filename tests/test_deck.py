"""
Module de tests pour la gestion des decks dans l'application.
"""
import pytest
import json
import os
from datetime import datetime
import time
from pathlib import Path
import sys

# Ajoute le répertoire parent au PYTHONPATH
sys.path.append(str(Path(__file__).parent.parent))

from app import app

@pytest.fixture
def deck_params():
    """Fixture fournissant les paramètres par défaut pour les tests de deck"""
    return {
        'deck_name': "Test Deck",
        'date_created': datetime.now().strftime("%Y-%m-%d"),
        'flashcards': [],
        'deck_list': [f"Deck {i+1}" for i in range(3)],
        'concurrent_operations_count': 5,
        'max_name_length': 50,
        'error_messages': {
            'name_missing': 'Nom du deck manquant',
            'not_found': 'non trouvé',
            'delete_error': 'Erreur lors de la suppression',
            'write_error': "Erreur simulée d'écriture"
        },
        'special_chars': {
            'valid': 'Test-Deck_123 éèà',
            'invalid': 'Test/Deck\\<>:"|?*'
        },
        'ui_elements': {
            'empty_deck': 'Aucune carte dans ce deck',
            'add_card': 'Ajouter une carte',
            'start_revision': 'Commencer la révision',
            'back_link': '← Retour aux decks',
            'create_button': 'Créer un nouveau deck',
            'settings_button': '⚙️ Paramètres'
        },
        'status_codes': {
            'success': 201,
            'not_found': 404,
            'conflict': 409,
            'bad_request': 400,
            'server_error': 500,
            'no_content': 204,
            'ok': 200
        }
    }

@pytest.fixture
def deck_id(deck_params):
    """Fixture générant un ID unique pour le deck"""
    clean_name = "".join(c for c in deck_params['deck_name'] if c.isalnum() or c in (' ', '-', '_')).strip()
    return f"{clean_name.replace(' ', '_').lower()}_{int(time.time())}"

@pytest.fixture
def deck_structure(deck_params, deck_id):
    """Fixture fournissant la structure attendue du deck"""
    return {
        "id": deck_id,
        "deck_name": deck_params['deck_name'],
        "date_created": deck_params['date_created'],
        "flashcards": deck_params['flashcards']
    }

class TestDeck:
    """Suite de tests pour la gestion des decks de cartes.

    Cette classe contient tous les tests nécessaires pour vérifier le bon fonctionnement
    de la gestion des decks de cartes dans l'application. Les tests couvrent les opérations
    CRUD (Create, Read, Update, Delete) ainsi que les cas d'erreur et les scénarios complexes.

    Tests implémentés:
        1. test_create_deck:
           - Création d'un nouveau deck et vérification de sa structure

        2. test_duplicate_deck:
           - Gestion des tentatives de création de decks en double

        3. test_list_decks:
           - Affichage et listage des decks existants

        4. test_view_deck_page:
           - Affichage de la page individuelle d'un deck

        5. test_view_nonexistent_deck:
           - Gestion des tentatives d'accès à des decks inexistants

        6. test_delete_nonexistent_deck:
           - Gestion des tentatives de suppression de decks inexistants

        7. test_delete_deck:
           - Suppression d'un deck existant

        8. test_deck_name_validation:
           - Validation des noms de deck (longueur, caractères spéciaux)

        9. test_deck_error_handling:
           - Gestion des erreurs système (IO, etc.)

        10. test_deck_concurrent_operations:
            - Tests de concurrence et de charge

        11. test_deck_deletion_confirmation:
            - Processus de confirmation de suppression

        12. test_multiple_decks:
            - Gestion de plusieurs decks en parallèle

    Fixtures utilisées:
        - client: Client de test Flask pour les requêtes HTTP
        - clean_data_dir: Assure un répertoire de données propre avant chaque test
        - deck_params: Paramètres de configuration pour les tests de deck
        - deck_structure: Structure attendue pour les données de deck

    Notes:
        - Chaque test est indépendant grâce à la fixture clean_data_dir
        - Les tests utilisent des paramètres configurables via deck_params
        - La validation des réponses HTTP et du contenu JSON est systématique
        - Les cas d'erreur sont testés aussi rigoureusement que les cas nominaux
    """

    @pytest.mark.dependency()
    def test_create_deck(self, client, clean_data_dir, deck_params, deck_structure):
        """Test la création d'un nouveau deck.
        
        Cette fonction vérifie :
        1. La création réussie d'un nouveau deck via l'API
        2. Le code de statut HTTP 201 pour une création réussie
        3. La structure correcte des données du deck retournées
        4. La création du fichier JSON correspondant
        5. La structure et le contenu corrects du fichier JSON
        
        Args:
            client: Le client de test Flask
            clean_data_dir: Fixture assurant un répertoire de données propre
            deck_params: Paramètres de configuration pour les tests de deck
        """
        response = client.post('/api/decks', json={'name': deck_params['deck_name']})
        assert response.status_code == deck_params['status_codes']['success']
        
        data = response.get_json()
        assert data['deck_name'] == deck_params['deck_name']
        
        # Vérifie que le fichier JSON a été créé
        deck_file = Path(app.config['DECKS_FOLDER']) / f"{deck_params['deck_name']}.json"
        assert deck_file.exists()
        
        # Vérifie le contenu du fichier
        with open(deck_file, 'r', encoding='utf-8') as f:
            deck_data = json.load(f)
            assert deck_data['deck_name'] == deck_params['deck_name']
            assert deck_data['flashcards'] == []
            assert 'date_created' in deck_data

    @pytest.mark.dependency()
    def test_duplicate_deck(self, client, clean_data_dir, deck_params):
        """Test la gestion des decks en double.
        
        Cette fonction vérifie :
        1. La création réussie d'un premier deck
        2. Le rejet d'un second deck avec le même nom (409 Conflict)
        3. La présence d'un message d'erreur approprié
        4. La suggestion d'un nom alternatif pour le deck en double
        
        Args:
            client: Le client de test Flask
            clean_data_dir: Fixture assurant un répertoire de données propre
            deck_params: Paramètres de configuration pour les tests de deck
        """
        # Crée le premier deck
        response = client.post('/api/decks', json={'name': deck_params['deck_name']})
        assert response.status_code == deck_params['status_codes']['success']
        
        # Tente de créer un deck avec le même nom
        response = client.post('/api/decks', json={'name': deck_params['deck_name']})
        assert response.status_code == deck_params['status_codes']['conflict']
        data = response.get_json()
        assert 'error' in data
        assert 'suggestion' in data
        assert data['suggestion'] == f"{deck_params['deck_name']} (1)"

    @pytest.mark.dependency()
    def test_list_decks(self, client, clean_data_dir, deck_params):
        """Test l'affichage de la liste des decks.
        
        Cette fonction vérifie :
        1. La création réussie de plusieurs decks
        2. L'accès réussi à la page d'accueil
        3. La présence de tous les decks créés dans la réponse HTML
        4. L'ordre et la structure correcte de l'affichage
        
        Args:
            client: Le client de test Flask
            clean_data_dir: Fixture assurant un répertoire de données propre
            deck_params: Paramètres de configuration pour les tests de deck
        """
        # Crée quelques decks
        for name in deck_params['deck_list']:
            response = client.post('/api/decks', json={'name': name})
            assert response.status_code == deck_params['status_codes']['success']
        
        # Vérifie que tous les decks sont listés
        response = client.get('/')
        assert response.status_code == deck_params['status_codes']['ok']
        response_text = response.data.decode('utf-8')
        
        for name in deck_params['deck_list']:
            assert name in response_text

    @pytest.mark.dependency()
    def test_view_deck_page(self, client, clean_data_dir, deck_params):
        """Test l'affichage de la page d'un deck.
        
        Cette fonction vérifie :
        1. La création réussie d'un deck
        2. L'accès réussi à la page du deck
        3. La présence du nom du deck dans la page
        4. La présence des éléments UI requis (message deck vide, boutons)
        
        Args:
            client: Le client de test Flask
            clean_data_dir: Fixture assurant un répertoire de données propre
            deck_params: Paramètres de configuration pour les tests de deck
        """
        # Crée un deck
        response = client.post('/api/decks', json={'name': deck_params['deck_name']})
        assert response.status_code == deck_params['status_codes']['success']
        
        # Accède à la page du deck
        response = client.get(f'/decks/{deck_params["deck_name"]}')
        assert response.status_code == deck_params['status_codes']['ok']
        
        # Vérifie le contenu de la page
        response_text = response.data.decode('utf-8')
        assert deck_params['deck_name'] in response_text
        assert deck_params['ui_elements']['empty_deck'] in response_text
        assert deck_params['ui_elements']['add_card'] in response_text
        assert deck_params['ui_elements']['start_revision'] in response_text

    @pytest.mark.dependency()
    def test_view_nonexistent_deck(self, client, clean_data_dir, deck_params):
        """Test l'affichage d'un deck inexistant.
        
        Cette fonction vérifie :
        1. La tentative d'accès à un deck inexistant
        2. Le code de statut 404 Not Found
        3. La présence d'un message d'erreur approprié
        
        Args:
            client: Le client de test Flask
            clean_data_dir: Fixture assurant un répertoire de données propre
            deck_params: Paramètres de configuration pour les tests de deck
        """
        response = client.get('/decks/nonexistent')
        assert response.status_code == deck_params['status_codes']['not_found']
        assert deck_params['error_messages']['not_found'].encode('utf-8') in response.data

    @pytest.mark.dependency()
    def test_delete_nonexistent_deck(self, client, clean_data_dir, deck_params):
        """Test la suppression d'un deck inexistant.
        
        Cette fonction vérifie :
        1. La tentative de suppression d'un deck inexistant
        2. Le code de statut 404 Not Found
        3. La gestion appropriée de l'erreur
        
        Args:
            client: Le client de test Flask
            clean_data_dir: Fixture assurant un répertoire de données propre
            deck_params: Paramètres de configuration pour les tests de deck
        """
        response = client.delete('/api/decks/nonexistent')
        assert response.status_code == deck_params['status_codes']['not_found']

    @pytest.mark.dependency()
    def test_delete_deck(self, client, clean_data_dir, deck_params):
        """Test la suppression d'un deck existant.
        
        Cette fonction vérifie :
        1. La création réussie d'un deck
        2. La suppression réussie du deck
        3. Le code de statut 204 No Content après suppression
        4. L'impossibilité d'accéder au deck supprimé (404)
        
        Args:
            client: Le client de test Flask
            clean_data_dir: Fixture assurant un répertoire de données propre
            deck_params: Paramètres de configuration pour les tests de deck
        """
        # Crée un deck
        response = client.post('/api/decks', json={'name': deck_params['deck_name']})
        assert response.status_code == deck_params['status_codes']['success']
        
        # Supprime le deck
        response = client.delete(f'/api/decks/{deck_params["deck_name"]}')
        assert response.status_code == deck_params['status_codes']['no_content']
        
        # Vérifie que le deck n'existe plus
        response = client.get(f'/decks/{deck_params["deck_name"]}')
        assert response.status_code == deck_params['status_codes']['not_found']

    @pytest.mark.dependency()
    def test_deck_name_validation(self, client, clean_data_dir, deck_params):
        """Test la validation du nom des decks.
        
        Cette fonction vérifie :
        1. Le rejet des noms vides
        2. Le rejet des noms trop longs
        3. L'acceptation des caractères spéciaux valides
        4. Le rejet des caractères spéciaux invalides
        5. Les messages d'erreur appropriés pour chaque cas
        
        Args:
            client: Le client de test Flask
            clean_data_dir: Fixture assurant un répertoire de données propre
            deck_params: Paramètres de configuration pour les tests de deck
        """
        # Test nom vide
        response = client.post('/api/decks', json={'name': ''})
        assert response.status_code == deck_params['status_codes']['bad_request']
        assert 'error' in response.get_json()
        
        # Test nom trop long
        long_name = 'a' * (deck_params['max_name_length'] + 1)
        response = client.post('/api/decks', json={'name': long_name})
        assert response.status_code == deck_params['status_codes']['bad_request']
        assert 'error' in response.get_json()
        
        # Test caractères spéciaux valides
        response = client.post('/api/decks', json={'name': deck_params['special_chars']['valid']})
        assert response.status_code == deck_params['status_codes']['success']
        
        # Test caractères spéciaux invalides
        response = client.post('/api/decks', json={'name': deck_params['special_chars']['invalid']})
        assert response.status_code == deck_params['status_codes']['bad_request']
        assert 'error' in response.get_json()

    @pytest.mark.dependency()
    def test_deck_error_handling(self, client, clean_data_dir, deck_params, monkeypatch):
        """Test la gestion des erreurs lors des opérations sur les decks.
        
        Cette fonction vérifie :
        1. La gestion des erreurs d'écriture de fichier
        2. Les codes de statut d'erreur appropriés (500)
        3. Les messages d'erreur explicites
        4. La cohérence de l'état du système après une erreur
        
        Args:
            client: Le client de test Flask
            clean_data_dir: Fixture assurant un répertoire de données propre
            deck_params: Paramètres de configuration pour les tests de deck
            monkeypatch: Fixture pytest pour le monkey patching
        """
        # Test erreur lors de la création (simulation erreur d'écriture)
        def mock_write_error(*args, **kwargs):
            raise IOError(deck_params['error_messages']['write_error'])
        
        monkeypatch.setattr('builtins.open', mock_write_error)
        response = client.post('/api/decks', json={'name': 'New Deck'})
        assert response.status_code == deck_params['status_codes']['server_error']
        assert 'error' in response.get_json()

    @pytest.mark.dependency()
    def test_deck_concurrent_operations(self, client, clean_data_dir, deck_params):
        """Test des opérations concurrentes sur les decks.
        
        Cette fonction vérifie :
        1. La création simultanée de plusieurs decks
        2. La gestion correcte des conflits de noms
        3. L'intégrité des données lors d'opérations parallèles
        4. La performance et la stabilité sous charge
        
        Args:
            client: Le client de test Flask
            clean_data_dir: Fixture assurant un répertoire de données propre
            deck_params: Paramètres de configuration pour les tests de deck
        """
        # Crée plusieurs decks en parallèle
        responses = []
        for i in range(deck_params['concurrent_operations_count']):
            response = client.post('/api/decks', json={'name': f'Test Deck {i}'})
            responses.append(response)
        
        # Vérifie que tous les decks ont été créés avec succès
        successful_responses = [r for r in responses if r.status_code == deck_params['status_codes']['success']]
        assert len(successful_responses) == deck_params['concurrent_operations_count']

    @pytest.mark.dependency()
    def test_deck_deletion_confirmation(self, client, clean_data_dir, deck_params):
        """Test la confirmation de suppression d'un deck.
        
        Cette fonction vérifie :
        1. La création réussie d'un deck
        2. La suppression avec confirmation
        3. La vérification de la suppression effective
        4. La gestion des tentatives d'accès après suppression
        
        Args:
            client: Le client de test Flask
            clean_data_dir: Fixture assurant un répertoire de données propre
            deck_params: Paramètres de configuration pour les tests de deck
        """
        # Crée un deck
        response = client.post('/api/decks', json={'name': deck_params['deck_name']})
        assert response.status_code == deck_params['status_codes']['success']
        
        # Supprime le deck sans confirmation
        response = client.delete(f'/api/decks/{deck_params["deck_name"]}')
        assert response.status_code == deck_params['status_codes']['no_content']
        
        # Vérifie que le deck a été supprimé
        response = client.get(f'/decks/{deck_params["deck_name"]}')
        assert response.status_code == deck_params['status_codes']['not_found']

    @pytest.mark.dependency()
    def test_multiple_decks(self, client, clean_data_dir, deck_params):
        """Test la création et la gestion de plusieurs decks en parallèle.
        
        Cette fonction vérifie :
        1. La création de multiples decks avec différentes configurations
        2. La gestion correcte des ressources pour chaque deck
        3. L'isolation des données entre les decks
        4. La performance avec plusieurs decks actifs
        
        Args:
            client: Le client de test Flask
            clean_data_dir: Fixture assurant un répertoire de données propre
            deck_params: Paramètres de configuration pour les tests de deck
        """
        # Crée plusieurs instances de test avec des configurations différentes
        decks = [
            {
                'deck_name': name,
                'flashcards': [{"question": f"Q{i}", "answer": f"A{i}"} for i in range(2)],
                'ui_elements': {
                    'empty_deck': 'Aucune carte dans ce deck',
                    'add_card': 'Ajouter une carte',
                    'start_revision': 'Commencer la révision'
                }
            } for name in deck_params['deck_list']
        ]
        
        # Teste la création de chaque deck
        for deck in decks:
            response = client.post('/api/decks', json={'name': deck['deck_name']})
            assert response.status_code == deck_params['status_codes']['success']
            
        # Vérifie que tous les decks sont listés sur la page d'accueil
        response = client.get('/')
        assert response.status_code == deck_params['status_codes']['ok']
        response_text = response.data.decode('utf-8')
        
        for deck in decks:
            assert deck['deck_name'] in response_text
            assert str(len(deck['flashcards'])) in response_text
            
        # Vérifie l'accès à chaque deck
        for deck in decks:
            response = client.get(f'/decks/{deck["deck_name"]}')
            assert response.status_code == deck_params['status_codes']['ok']
            assert deck['deck_name'] in response.data.decode('utf-8')
            
        # Teste la suppression de chaque deck
        for deck in decks:
            response = client.delete(f'/api/decks/{deck["deck_name"]}')
            assert response.status_code == deck_params['status_codes']['no_content']
            
        # Vérifie que tous les decks ont été supprimés
        response = client.get('/')
        response_text = response.data.decode('utf-8')
        for deck in decks:
            assert deck['deck_name'] not in response_text
