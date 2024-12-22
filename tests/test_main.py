"""
Point d'entrée principal pour l'exécution des tests
"""
import pytest

# Import de tous les tests
from .test_app import *
from .test_deck import *
from .test_cards import *
from .test_difficulty import *
from .test_flows import *

class TestMain:
    """
    Classe principale de tests qui contient tous les tests de l'application
    """
    
    def test_run_all_tests(self):
        """
        Fonction principale pour exécuter tous les tests dans l'ordre
        Cette fonction peut être appelée directement ou via pytest
        """
        
        # ===== Tests de base de l'application =====
        self.test_home_page()              # Vérifie le chargement de la page d'accueil et son contenu
        self.test_create_deck_page()       # Vérifie le chargement de la page de création de deck
        
        # ===== Tests des paramètres de difficulté =====
        self.test_difficulty_page_load()           # Vérifie le chargement de la page des paramètres
        self.test_default_difficulty_values()      # Vérifie les valeurs par défaut des niveaux
        self.test_unit_conversion_and_validation() # Vérifie la conversion entre minutes, heures et jours
        self.test_minimum_difference_validation()  # Vérifie les écarts minimums entre niveaux
        self.test_mixed_units_validation()        # Vérifie la gestion des unités mixtes
        self.test_settings_persistence()          # Vérifie la sauvegarde et restauration des paramètres
        
        # ===== Tests de gestion des decks =====
        self.test_create_deck()            # Vérifie la création d'un nouveau deck
        self.test_duplicate_deck()         # Vérifie la gestion des noms en double
        self.test_list_decks()            # Vérifie l'affichage de la liste des decks
        self.test_view_deck_page()        # Vérifie l'affichage d'un deck spécifique
        self.test_view_nonexistent_deck() # Vérifie la gestion des decks inexistants
        self.test_delete_deck()           # Vérifie la suppression d'un deck
        self.test_deck_name_validation()  # Vérifie la validation des noms de deck
        self.test_deck_error_handling()   # Vérifie la gestion des erreurs
        
        # ===== Tests de gestion des cartes (à implémenter) =====
        """
        # Tests basiques des cartes
        self.test_add_basic_card()        # Création d'une carte question/réponse simple
        self.test_edit_basic_card()       # Modification d'une carte existante
        self.test_delete_card()           # Suppression d'une carte
        
        # Tests des types spéciaux de cartes
        self.test_add_mcq_card()          # Création de carte QCM avec validation des options
        self.test_add_code_card()         # Création de carte avec bloc de code et coloration syntaxique
        self.test_add_free_input_card()   # Création de carte avec validation de saisie libre
        
        # Tests du système de révision
        self.test_start_revision()        # Démarrage d'une session de révision
        self.test_card_scheduling()       # Vérification de l'ordre des cartes selon la difficulté
        self.test_revision_progress()     # Suivi de la progression dans une session
        
        # Tests des tags et catégories
        self.test_add_tags()             # Ajout et validation des tags
        self.test_filter_by_tags()       # Filtrage des cartes par tags
        self.test_manage_categories()    # Gestion des catégories de cours
        
        # Tests de performance
        self.test_large_deck_loading()   # Chargement d'un deck avec nombreuses cartes
        self.test_multiple_decks()       # Gestion de multiples decks simultanés
        self.test_concurrent_users()     # Simulation d'utilisateurs multiples
        """

if __name__ == '__main__':
    pytest.main(['-v', '--dependency-mode=strict'])
