# Smart Revision App 📚

## Démonstration

https://user-images.githubusercontent.com/YGueguen16u/smart-revision-app/presentation/smart_revision_app.mp4

Vous pouvez également voir la vidéo directement dans le dossier [presentation/smart_revision_app.mp4](presentation/smart_revision_app.mp4)

*Regardez la vidéo de démonstration ci-dessus pour voir l'application en action !*

## À propos

Smart Revision App est une application moderne de révision par cartes, conçue pour optimiser votre apprentissage grâce à un système de répétition espacée intelligent. Que vous étudiiez du code, des langues ou tout autre sujet, notre application s'adapte à votre rythme d'apprentissage.

## Fonctionnalités ✨

- **Types de cartes variés**
  - Cartes traditionnelles (recto-verso)
  - Cartes de code (avec validation Python, SQL, Bash)
  - Questions à choix multiples
  - Saisie libre avec validation

- **Système de révision intelligent**
  - Algorithme de répétition espacée (basé sur SM-2)
  - Adaptation automatique aux performances
  - 5 niveaux de difficulté configurables

- **Organisation efficace**
  - Gestion par decks
  - Tags hiérarchiques
  - Export des cours en Markdown

- **Interface moderne**
  - Design responsive
  - Support du Markdown
  - Intégration multimédia (images, audio, vidéo)

## Installation 🚀

### Avec Docker (recommandé)

```bash
# Cloner le repository
git clone https://github.com/YGueguen16u/smart-revision-app.git
cd smart-revision-app

# Lancer avec Docker Compose
docker-compose up --build
```

### Installation manuelle

```bash
# Cloner le repository
git clone https://github.com/YGueguen16u/smart-revision-app.git
cd smart-revision-app

# Installer les dépendances Python
python -m pip install -r requirements.txt

# Installer les dépendances Node.js
npm install

# Lancer l'application
python app.py
```

L'application sera accessible à l'adresse : http://localhost:8000

### Lancement rapide (Windows)

Un script `activate.bat` est fourni pour lancer rapidement l'application sous Windows :

1. Double-cliquez simplement sur `activate.bat`
   ou
2. Dans une console :
```bash
activate.bat
```

L'application démarrera automatiquement et sera accessible à l'adresse : http://localhost:8000

## Développement 🛠️

### Tests

```bash
pytest tests/
```

### CI/CD

Le projet utilise GitHub Actions pour :
- Exécuter les tests automatiquement
- Générer les rapports de couverture
- Construire et publier l'image Docker

## Contribution 🤝

Les contributions sont les bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## Licence 📄

MIT
