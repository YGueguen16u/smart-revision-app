# Structure des Tests - Smart Revision App

## Vue d'ensemble
Ce document définit la structure et l'ordre d'exécution des tests pour l'application Smart Revision. Les tests sont organisés de manière hiérarchique, avec des dépendances clairement définies entre chaque niveau de test.

## 1. Tests de Base de l'Application
### 1.1. Navigation de Base
1. **Test de la Page d'Accueil** [T1.1.1]
   - Vérifier le chargement correct de la page d'accueil
   - Vérifier la présence des éléments de navigation
   - Vérifier l'affichage du titre "Mes Decks de Révision"

### 1.2. Configuration Initiale
1. **Test des Paramètres de Difficulté** [T1.2.1]
   - Vérifier l'accès aux paramètres
   - Configurer les intervalles de révision :
     - Très difficile : 3 minutes
     - Difficile : 5 minutes
     - Moyen : 7 minutes
     - Facile : 9 minutes
     - Très facile : 11 minutes
   - Vérifier la sauvegarde des paramètres

## 2. Tests de Gestion des Decks
### 2.1. Création et Configuration des Decks
1. **Test de la Page de Création de Deck** [T2.1.1]
   - Vérifier le chargement de la page de création
   - Vérifier la présence du formulaire

2. **Tests de Création de Decks** [T2.1.2]
   - Créer le premier deck "Mathématiques"
   - Créer le second deck "Physique"
   - Vérifier la création réussie des deux decks

3. **Test de Duplication** [T2.1.3]
   - Tenter de créer un deck "Mathématiques" (même nom)
   - Vérifier la gestion des doublons
   - Vérifier la suggestion de nom alternatif

4. **Test de Configuration des Decks** [T2.1.4]
   - Configurer les paramètres spécifiques du deck
   - Vérifier la sauvegarde des configurations

### 2.2. Gestion des Decks
1. **Test de Listage des Decks** [T2.2.1]
   - Vérifier l'affichage de tous les decks créés
   - Vérifier les informations affichées pour chaque deck

## 3. Tests des Cartes
### 3.1. Cartes Traditionnelles
1. **Tests de Création et Révision** [T3.1.1]
   - Créer 5 cartes avec différents niveaux de difficulté
   - Test de révision pour chaque carte :
     - Carte 1 : Très difficile (3 min)
     - Carte 2 : Difficile (5 min)
     - Carte 3 : Moyenne (7 min)
     - Carte 4 : Facile (9 min)
     - Carte 5 : Très facile (11 min)

2. **Tests de Suivi Temporel** [T3.1.2]
   - Vérifier l'état des cartes toutes les minutes pendant 11 minutes
   - Pour chaque minute :
     - Vérifier "Toutes les cartes"
     - Vérifier "À réviser maintenant"
     - Vérifier "À réviser plus tard"

3. **Tests de Suppression** [T3.1.3]
   - Supprimer les cartes une par une
   - Vérifier la mise à jour de la liste après chaque suppression

### 3.2. Types de Cartes Spéciaux
1. **Test des Cartes MCQ** [T3.2.1]
   - Créer une carte QCM
   - Tester la carte
   - Supprimer la carte

2. **Test des Cartes à Saisie Libre** [T3.2.2]
   - Créer une carte à saisie libre
   - Tester la carte
   - Supprimer la carte

3. **Tests des Cartes Code** [T3.2.3]
   - Test carte Python
   - Test carte SQL
   - Test carte Linux
   Pour chaque type :
   - Créer la carte
   - Vérifier la coloration syntaxique
   - Tester l'exécution/validation
   - Supprimer la carte

### 3.3. Organisation et Tags
1. **Tests de Structure** [T3.3.1]
   - Créer 5 cartes avec tags et sous-tags
   - Vérifier la hiérarchie des tags
   - Vérifier le filtrage par tags

2. **Tests de Cours** [T3.3.2]
   - Créer un cours avec les cartes taggées
   - Vérifier la structure du cours
   - Supprimer le cours
   - Vérifier que les cartes restent intactes

3. **Nettoyage Final** [T3.3.3]
   - Supprimer toutes les cartes restantes
   - Vérifier l'état final du deck

## Tests des paramètres de difficulté

### Test de la gestion des unités et des valeurs

1. **Test des conversions automatiques**
   - Test des minutes vers heures :
     * Entrer 59 minutes (doit rester en minutes)
     * Entrer 60 minutes (doit passer à 1 heure)
     * Entrer 120 minutes (doit afficher 2 heures)
   - Test des heures vers jours :
     * Entrer 23 heures (doit rester en heures)
     * Entrer 24 heures (doit passer à 1 jour)
     * Entrer 48 heures (doit afficher 2 jours)
   - Vérifier que les autres niveaux s'ajustent en conséquence

2. **Test de la cohérence et progression**
   - Test avec unités mixtes :
     * "Très difficile" : 30 minutes
     * "Difficile" : 2 heures
     * "Moyen" : 3 heures
     * "Facile" : 1 jour
     * "Très facile" : 2 jours
   - Vérifier que l'ordre croissant est maintenu
   - Vérifier les différences minimales entre niveaux :
     * 60 minutes minimum entre niveaux en minutes
     * 2 heures minimum entre niveaux en heures
     * 1 jour minimum entre niveaux en jours

3. **Test des ajustements automatiques**
   - Essayer de définir des valeurs invalides :
     * Mettre "Facile" inférieur à "Difficile"
     * Mettre "Très facile" égal à "Facile"
   - Vérifier les corrections automatiques :
     * Les valeurs doivent être ajustées pour maintenir l'ordre
     * Les différences minimales doivent être respectées

4. **Test des changements d'unité manuels**
   - Définir une valeur en minutes
   - Changer manuellement l'unité en heures
   - Changer manuellement l'unité en jours
   - Revenir aux minutes
   - Vérifier à chaque étape :
     * La conversion est correcte
     * L'ordre est maintenu
     * Les différences minimales sont respectées

5. **Test des valeurs invalides**
   - Essayer d'entrer :
     * Des valeurs négatives
     * Zéro
     * Des caractères non numériques
   - Vérifier que ces valeurs sont rejetées
   - Vérifier que la valeur minimale (1) est appliquée

6. **Test de persistance**
   - Configurer différents niveaux avec différentes unités
   - Sauvegarder les paramètres
   - Recharger la page
   - Vérifier :
     * Les valeurs sont correctement restaurées
     * Les unités sont conservées
     * L'ordre et les différences sont maintenus

## 4. Tests de Performance et Limites
### 4.1. Tests de Charge
1. **Test de Limite de Cartes** [T4.1.1]
   - Créer un grand nombre de cartes
   - Vérifier les performances de chargement
   - Vérifier les performances de recherche

### 4.2. Tests de Robustesse
1. **Test de Récupération** [T4.2.1]
   - Simuler des interruptions pendant les opérations
   - Vérifier la récupération des données

## Notes d'Implémentation
- Chaque test doit être indépendant et idempotent
- Les tests sont exécutés dans l'ordre spécifié
- Utilisation de pytest-dependency pour gérer les dépendances
- Les identifiants entre crochets [Tx.x.x] sont utilisés dans le code des tests

## Dépendances Critiques
- T1.1.1 → T2.1.1 → T2.1.2 → T2.1.3
- T1.2.1 requis pour tous les tests de révision
- T3.1.1 requis pour T3.1.2
- Tous les tests de création doivent précéder les tests de suppression correspondants
