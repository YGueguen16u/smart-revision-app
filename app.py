from flask import Flask, render_template, request, jsonify, url_for, redirect
import json
import os
import pathlib
import uuid
import time
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__, static_url_path='/static', static_folder='static')

# Dossier data du projet pour la config
project_data_dir = pathlib.Path(__file__).parent / 'data'
project_config_dir = project_data_dir / 'config'

# Dossier utilisateur pour les decks
user_home = pathlib.Path.home()
app_data_dir = user_home / 'SmartRevisionApp'
data_dir = app_data_dir / 'data'
decks_dir = data_dir / 'decks'
multimedia_dir = data_dir / 'multimedia'

# Création des dossiers
project_data_dir.mkdir(exist_ok=True)
project_config_dir.mkdir(exist_ok=True)
app_data_dir.mkdir(exist_ok=True)
data_dir.mkdir(exist_ok=True)
decks_dir.mkdir(exist_ok=True)
multimedia_dir.mkdir(exist_ok=True)

# Configuration pour l'upload de fichiers
MULTIMEDIA_FOLDER = str(multimedia_dir)
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_AUDIO_EXTENSIONS = {'mp3', 'wav', 'ogg'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'webm', 'ogg'}

# Créer les dossiers multimedia s'ils n'existent pas
os.makedirs(os.path.join(MULTIMEDIA_FOLDER, 'images'), exist_ok=True)
os.makedirs(os.path.join(MULTIMEDIA_FOLDER, 'audio'), exist_ok=True)
os.makedirs(os.path.join(MULTIMEDIA_FOLDER, 'video'), exist_ok=True)

app.config['DATA_FOLDER'] = str(data_dir)
app.config['DECKS_FOLDER'] = str(decks_dir)
app.config['CONFIG_FOLDER'] = str(project_config_dir)
app.config['MULTIMEDIA_FOLDER'] = MULTIMEDIA_FOLDER

def get_all_decks():
    """Récupère tous les decks"""
    decks = []
    try:
        for file in decks_dir.glob('*.json'):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    deck = json.load(f)
                    deck['id'] = file.stem
                    decks.append(deck)
            except Exception as e:
                print(f"Error reading deck {file}: {e}")
                continue
    except Exception as e:
        print(f"Error scanning decks directory: {e}")
    return decks

def get_deck(deck_id):
    """Récupère un deck par son ID"""
    file_path = decks_dir / f"{deck_id}.json"
    if not file_path.exists():
        return None
    
    with open(file_path, 'r', encoding='utf-8') as f:
        deck = json.load(f)
        deck['id'] = deck_id
        return deck

def save_deck(deck_data):
    # Nettoie le nom du deck pour l'utiliser comme nom de fichier
    clean_name = "".join(c for c in deck_data['name'] if c.isalnum() or c in (' ', '-', '_')).strip()
    clean_name = clean_name.replace(' ', '_').lower()
    
    # Ajoute un timestamp pour garantir l'unicité
    timestamp = time.time()
    deck_id = f"{clean_name}_{int(timestamp)}"
    
    # Crée les données du deck
    deck = {
        "id": deck_id,
        "deck_name": deck_data['name'],
        "date_created": timestamp,
        "flashcards": []
    }
    
    # Crée le fichier JSON
    file_path = decks_dir / f"{deck_id}.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(deck, f, ensure_ascii=False, indent=2)
    
    return deck

def delete_deck_file(deck_id):
    file_path = decks_dir / f"{deck_id}.json"
    if file_path.exists():
        file_path.unlink()
        return True
    return False

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def save_uploaded_file(file, subfolder):
    if file and file.filename:
        filename = secure_filename(file.filename)
        unique_filename = f"{str(uuid.uuid4())}_{filename}"
        file_path = os.path.join(MULTIMEDIA_FOLDER, subfolder, unique_filename)
        file.save(file_path)
        return os.path.join('multimedia', subfolder, unique_filename)
    return None

@app.route('/')
def home():
    decks = get_all_decks()
    return render_template('index.html', decks=decks)

@app.route('/create-deck')
def create_deck_page():
    return render_template('create_deck.html')

@app.route('/api/decks', methods=['POST'])
def create_deck():
    """Crée un nouveau deck"""
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({'error': 'Nom du deck manquant'}), 400
        
    deck_name = data['name']
    
    # Nettoie le nom du deck pour l'utiliser comme nom de fichier
    clean_name = "".join(c for c in deck_name if c.isalnum() or c in (' ', '-', '_')).strip()
    clean_name = clean_name.replace(' ', '_').lower()
    
    # Vérifier si un deck avec ce nom existe déjà
    deck_path = decks_dir / f"{clean_name}.json"
    if deck_path.exists():
        return jsonify({
            'error': 'Un deck avec ce nom existe déjà',
            'suggestion': f"{deck_name} ({len(list(decks_dir.glob('*.json')))})"
        }), 409
    
    # Créer le nouveau deck
    deck = {
        'deck_name': deck_name,
        'flashcards': [],
        'date_created': time.time()
    }
    
    # Sauvegarder le deck
    try:
        with open(deck_path, 'w', encoding='utf-8') as f:
            json.dump(deck, f, ensure_ascii=False, indent=4)
        print(f"Deck saved to: {deck_path}")
    except Exception as e:
        print(f"Error saving deck: {e}")
        return jsonify({'error': 'Erreur lors de la sauvegarde du deck'}), 500
    
    return jsonify(deck), 201

@app.route('/decks/<deck_name>')
def view_deck(deck_name):
    """Affiche un deck spécifique."""
    deck = get_deck(deck_name)
    if deck is None:
        return redirect('/')
    
    # Ajouter le nom du deck aux données
    deck['name'] = deck_name
    
    current_time = int(time.time())
    cards_to_review_now = []
    cards_to_review_later = []

    for card in deck.get('flashcards', []):
        next_review = card.get('next_review', 0)
        if next_review <= current_time:
            cards_to_review_now.append(card)
        else:
            card['next_review_display'] = datetime.fromtimestamp(next_review).strftime('%d/%m/%Y %H:%M')
            cards_to_review_later.append(card)
    
    # Trier les cartes à réviser plus tard par date de révision croissante
    cards_to_review_later.sort(key=lambda x: x.get('next_review', 0))

    return render_template('deck.html', 
                         deck=deck,
                         cards_to_review_now=cards_to_review_now,
                         cards_to_review_later=cards_to_review_later)

@app.route('/decks/<deck_id>/add-card')
def add_card_page(deck_id):
    """Page d'ajout de carte"""
    deck = get_deck(deck_id)
    if deck is None:
        return redirect('/')
    return render_template('add_card.html', deck=deck)

@app.route('/api/decks/<deck_id>/cards', methods=['POST'])
def add_card(deck_id):
    """Ajoute une carte à un deck"""
    deck = get_deck(deck_id)
    if deck is None:
        return jsonify({'error': 'Deck non trouvé'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Données manquantes'}), 400

    # Générer un ID unique pour la carte
    card_id = f"flashcard_{str(uuid.uuid4())[:8]}"
    
    # Créer la nouvelle carte
    new_card = {
        "id": card_id,
        "type": data.get('type', 'traditional'),
        "question": data.get('question'),
        "response": data.get('response'),
        "tags": data.get('tags', []),
        "feedback": data.get('feedback', ''),
        "difficulty": data.get('difficulty', 'Medium'),
        "date_created": data.get('date_created'),
        "date_last_reviewed": data.get('date_last_reviewed'),
        "date_next_review": data.get('date_next_review'),
        "statistics": data.get('statistics', {"successes": 0, "failures": 0}),
        "multimedia": data.get('multimedia', {"image": None, "audio": None, "video": None})
    }

    # Ajouter la carte au deck
    if 'flashcards' not in deck:
        deck['flashcards'] = []
    deck['flashcards'].append(new_card)

    # Sauvegarder le deck
    deck_path = decks_dir / f"{deck_id}.json"
    with open(deck_path, 'w', encoding='utf-8') as f:
        json.dump(deck, f, ensure_ascii=False, indent=2)

    return jsonify(new_card), 201

@app.route('/api/decks/<deck_id>', methods=['DELETE'])
def delete_deck(deck_id):
    if delete_deck_file(deck_id):
        return '', 204
    return jsonify({'error': 'Deck non trouvé'}), 404

@app.route('/api/decks/<deck_id>/cards', methods=['POST'])
def add_card_api(deck_id):
    if not request.files and not request.form:
        return jsonify({'error': 'Aucune donnée reçue'}), 400

    try:
        deck = get_deck(deck_id)
        if deck is None:
            return jsonify({'error': 'Deck non trouvé'}), 404

        # Récupérer les données du formulaire
        question = request.form.get('question')
        response = request.form.get('response')
        if not question or not response:
            return jsonify({'error': 'Question et réponse sont requises'}), 400

        # Créer la nouvelle carte
        new_card = {
            'id': f"flashcard_{str(uuid.uuid4()).replace('-', '')}",
            'type': 'traditional',
            'question': question,
            'response': response,
            'feedback': request.form.get('feedback', ''),
            'tags': json.loads(request.form.get('tags', '[]')),
            'difficulty': 'Medium',
            'date_created': datetime.now().strftime("%Y-%m-%d"),
            'date_last_reviewed': datetime.now().strftime("%Y-%m-%d"),
            'date_next_review': datetime.now().strftime("%Y-%m-%d"),
            'statistics': {
                'successes': 0,
                'failures': 0
            },
            'multimedia': {
                'image': None,
                'audio': None,
                'video': None
            }
        }

        # Gérer les fichiers uploadés
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename, ALLOWED_IMAGE_EXTENSIONS):
                new_card['multimedia']['image'] = save_uploaded_file(file, 'images')

        if 'audio' in request.files:
            file = request.files['audio']
            if file and file.filename and allowed_file(file.filename, ALLOWED_AUDIO_EXTENSIONS):
                new_card['multimedia']['audio'] = save_uploaded_file(file, 'audio')

        if 'video' in request.files:
            file = request.files['video']
            if file and file.filename and allowed_file(file.filename, ALLOWED_VIDEO_EXTENSIONS):
                new_card['multimedia']['video'] = save_uploaded_file(file, 'video')

        # Ajouter la carte au deck
        if 'flashcards' not in deck:
            deck['flashcards'] = []
        deck['flashcards'].append(new_card)
        save_deck(deck)

        return jsonify(new_card), 201

    except Exception as e:
        print(f"Erreur lors de l'ajout de la carte: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/decks/<deck_name>/cards/<card_id>', methods=['DELETE'])
def delete_card(deck_name, card_id):
    """Supprime une carte d'un deck"""
    try:
        # Charger le deck
        deck_path = decks_dir / f"{deck_name}.json"
        if not deck_path.exists():
            return jsonify({'error': 'Deck non trouvé'}), 404

        with open(deck_path, 'r', encoding='utf-8') as f:
            deck = json.load(f)

        # Vérifier si la carte existe
        found = False
        new_flashcards = []
        for card in deck['flashcards']:
            if str(card.get('id')) == str(card_id):
                found = True
            else:
                new_flashcards.append(card)

        if not found:
            return jsonify({'error': 'Carte non trouvée'}), 404

        # Mettre à jour le deck avec la carte supprimée
        deck['flashcards'] = new_flashcards
        
        # Sauvegarder le deck
        with open(deck_path, 'w', encoding='utf-8') as f:
            json.dump(deck, f, ensure_ascii=False, indent=2)

        return jsonify({'success': True}), 200

    except Exception as e:
        print(f"Erreur lors de la suppression de la carte: {e}")
        return jsonify({'error': 'Erreur lors de la suppression'}), 500

@app.route('/api/config')
def get_config():
    """Récupère la configuration des niveaux de difficulté"""
    config_path = project_config_dir / 'config.json'
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return jsonify(json.load(f))
    except FileNotFoundError:
        return jsonify({'error': 'Configuration non trouvée'}), 404

@app.route('/api/config/difficulty', methods=['POST'])
def update_difficulty():
    """Met à jour le temps limite pour un niveau de difficulté"""
    config_path = project_config_dir / 'config.json'
    
    try:
        # Charger la configuration existante
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        data = request.get_json()
        level = data.get('level')
        time_limit = data.get('time_limit')
        
        if not level or not time_limit:
            return jsonify({'error': 'Paramètres manquants'}), 400
            
        if level not in config['difficulty_levels']:
            return jsonify({'error': 'Niveau de difficulté invalide'}), 400
            
        # Mettre à jour le temps limite
        config['difficulty_levels'][level]['time_limit'] = time_limit
        
        # Sauvegarder la configuration
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
            
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Routes pour les paramètres de difficulté
@app.route('/settings/difficulty')
def difficulty_settings_page():
    """Affiche la page des paramètres de difficulté."""
    response = get_difficulty_settings()
    settings = response.get_json() if response.status_code == 200 else {}
    return render_template('difficulty_settings.html', settings=settings)

@app.route('/api/settings/difficulty', methods=['GET'])
def get_difficulty_settings():
    """Récupère les paramètres de difficulté"""
    config_path = project_config_dir / 'config.json'
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            return jsonify(config['difficulty_levels'])
    except FileNotFoundError:
        # Valeurs par défaut
        default_settings = {
            'very_hard': 3,
            'hard': 5,
            'medium': 7,
            'easy': 9,
            'very_easy': 11
        }
        # Sauvegarder les valeurs par défaut
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump({'difficulty_levels': default_settings}, f, indent=4, ensure_ascii=False)
        return jsonify(default_settings)

@app.route('/api/settings/difficulty', methods=['POST'])
def update_difficulty_settings():
    """Met à jour les paramètres de difficulté"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Données manquantes'}), 400

    # Validation des données
    required_levels = ['very_hard', 'hard', 'medium', 'easy', 'very_easy']
    if not all(level in data for level in required_levels):
        return jsonify({'error': 'Niveaux de difficulté manquants'}), 400

    # Vérification de l'ordre des temps
    times = [(level, data[level]) for level in required_levels]
    for i in range(len(times)-1):
        if times[i][1] >= times[i+1][1]:
            return jsonify({
                'error': f'Le temps pour {times[i][0]} doit être inférieur à {times[i+1][0]}'
            }), 400

    # Sauvegarde des paramètres
    config_path = project_config_dir / 'config.json'
    try:
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
        else:
            config = {}

        config['difficulty_levels'] = data
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
            
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/decks/<deck_id>/review')
def start_review(deck_id):
    """Démarre une session de révision pour un deck"""
    deck = get_deck(deck_id)
    if deck is None:
        return redirect('/')
    
    current_time = int(time.time())
    cards_to_review = [card for card in deck.get('flashcards', []) 
                      if card.get('next_review', 0) <= current_time]
    
    if not cards_to_review:
        return redirect(f'/decks/{deck_id}')
        
    return render_template('review.html', deck=deck, cards=cards_to_review)

@app.route('/api/decks/<deck_name>/cards/<card_id>/review', methods=['POST'])
def update_card_review(deck_name, card_id):
    """Met à jour une carte après une révision"""
    data = request.get_json()
    if not data or 'quality' not in data or 'next_interval' not in data:
        return jsonify({'error': 'Données manquantes'}), 400
        
    deck = get_deck(deck_name)
    if deck is None:
        return jsonify({'error': 'Deck non trouvé'}), 404
        
    # Trouver la carte
    card = None
    for c in deck['flashcards']:
        if str(c.get('id')) == str(card_id):
            card = c
            break
            
    if card is None:
        return jsonify({'error': 'Carte non trouvée'}), 404
        
    # Mettre à jour les statistiques de la carte
    if data['quality'] >= 3:
        card['statistics']['successes'] = card['statistics'].get('successes', 0) + 1
    else:
        card['statistics']['failures'] = card['statistics'].get('failures', 0) + 1
        
    # Mettre à jour les dates de révision
    current_time = int(time.time())
    card['date_last_reviewed'] = current_time
    card['next_review'] = current_time + (data['next_interval'] * 60)  # Convertir minutes en secondes
    
    # Sauvegarder le deck
    deck_path = decks_dir / f"{deck_name}.json"
    with open(deck_path, 'w', encoding='utf-8') as f:
        json.dump(deck, f, ensure_ascii=False, indent=2)
        
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)