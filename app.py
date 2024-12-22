from flask import Flask, render_template, request, jsonify, url_for, redirect
import json
import os
import pathlib
import uuid
import time
from datetime import datetime

app = Flask(__name__, static_url_path='/static', static_folder='static')

# Dossier data du projet pour la config
project_data_dir = pathlib.Path(__file__).parent / 'data'
project_config_dir = project_data_dir / 'config'

# Dossier utilisateur pour les decks
user_home = pathlib.Path.home()
app_data_dir = user_home / 'SmartRevisionApp'
data_dir = app_data_dir / 'data'
decks_dir = data_dir / 'decks'

# Création des dossiers
project_data_dir.mkdir(exist_ok=True)
project_config_dir.mkdir(exist_ok=True)
app_data_dir.mkdir(exist_ok=True)
data_dir.mkdir(exist_ok=True)
decks_dir.mkdir(exist_ok=True)

app.config['DATA_FOLDER'] = str(data_dir)
app.config['DECKS_FOLDER'] = str(decks_dir)
app.config['CONFIG_FOLDER'] = str(project_config_dir)

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

    # Séparer les cartes en deux catégories
    current_time = time.time()
    cards_to_review_now = []
    cards_to_review_later = []

    for card in deck.get('flashcards', []):
        next_review = card.get('next_review', 0)
        if next_review <= current_time:
            cards_to_review_now.append(card)
        else:
            # Formater la date de prochaine révision
            card['next_review'] = datetime.fromtimestamp(next_review).strftime('%d/%m/%Y %H:%M')
            cards_to_review_later.append(card)

    return render_template('deck.html', 
                         deck=deck, 
                         cards_to_review_now=cards_to_review_now,
                         cards_to_review_later=cards_to_review_later)

@app.route('/api/decks/<deck_id>', methods=['DELETE'])
def delete_deck(deck_id):
    if delete_deck_file(deck_id):
        return '', 204
    return jsonify({'error': 'Deck non trouvé'}), 404

@app.route('/api/decks/<deck_id>/cards', methods=['POST'])
def add_card(deck_id):
    """Ajoute une carte à un deck"""
    deck = get_deck(deck_id)
    if deck is None:
        return jsonify({'error': 'Deck non trouvé'}), 404
    
    data = request.json
    card = {
        'id': str(uuid.uuid4()),
        'question': data['question'],
        'answer': data['answer'],
        'created_at': datetime.now().strftime("%Y-%m-%d")
    }
    
    # Ajoute la carte au deck
    deck['flashcards'].append(card)
    
    # Sauvegarde le deck
    file_path = decks_dir / f"{deck_id}.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(deck, f, ensure_ascii=False, indent=2)
    
    return jsonify(card), 201

@app.route('/api/decks/<deck_id>/cards/<card_id>', methods=['PUT'])
def update_card(deck_id, card_id):
    """Modifie une carte existante"""
    deck = get_deck(deck_id)
    if deck is None:
        return jsonify({'error': 'Deck non trouvé'}), 404
    
    data = request.json
    for card in deck['flashcards']:
        if card['id'] == card_id:
            card['question'] = data['question']
            card['answer'] = data['answer']
            
            # Sauvegarde le deck
            file_path = decks_dir / f"{deck_id}.json"
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(deck, f, ensure_ascii=False, indent=2)
            
            return jsonify(card), 200
    
    return jsonify({'error': 'Carte non trouvée'}), 404

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

if __name__ == '__main__':
    app.run(debug=True)