// Variables globales
let cards = [];
let currentCardIndex = 0;
let difficultyLevels = null;

// Initialisation
async function initializeReview(initialCards) {
    cards = initialCards;
    
    // Charger les niveaux de difficulté
    try {
        const response = await fetch('/api/settings/difficulty');
        if (response.ok) {
            difficultyLevels = await response.json();
        }
    } catch (error) {
        console.error('Erreur lors du chargement des paramètres de difficulté:', error);
    }
    
    showNextCard();
}

function showNextCard() {
    if (currentCardIndex >= cards.length) {
        // Fin de la session
        window.location.href = `/decks/${deckName}`;
        return;
    }
    
    const card = cards[currentCardIndex];
    document.getElementById('questionText').textContent = card.question;
    document.getElementById('answerText').textContent = card.response;
    
    // Reset display
    document.getElementById('answerContainer').style.display = 'none';
    document.getElementById('showAnswerBtn').style.display = 'block';
    document.getElementById('feedbackBtns').style.display = 'none';
}

function showAnswer() {
    document.getElementById('answerContainer').style.display = 'block';
    document.getElementById('showAnswerBtn').style.display = 'none';
    document.getElementById('feedbackBtns').style.display = 'block';
}

async function submitFeedback(quality) {
    const card = cards[currentCardIndex];
    
    // Calculer le prochain intervalle de révision basé sur la difficulté
    let nextInterval;
    switch(quality) {
        case 1: // Très difficile
            nextInterval = difficultyLevels.very_hard;
            break;
        case 2: // Difficile
            nextInterval = difficultyLevels.hard;
            break;
        case 3: // Moyen
            nextInterval = difficultyLevels.medium;
            break;
        case 4: // Facile
            nextInterval = difficultyLevels.easy;
            break;
        case 5: // Très facile
            nextInterval = difficultyLevels.very_easy;
            break;
        default:
            nextInterval = difficultyLevels.medium;
    }
    
    try {
        const response = await fetch(`/api/decks/${deckName}/cards/${card.id}/review`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                quality: quality,
                next_interval: nextInterval
            })
        });
        
        if (response.ok) {
            currentCardIndex++;
            showNextCard();
        } else {
            alert('Erreur lors de la mise à jour de la carte');
        }
    } catch (error) {
        console.error('Erreur:', error);
        alert('Erreur lors de la mise à jour de la carte');
    }
}
