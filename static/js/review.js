// Variables globales
let cards = [];
let currentCardIndex = 0;
let difficultyLevels = null;

// Initialisation
async function initializeReview(initialCards) {
    console.log("Initialisation avec les cartes:", initialCards);
    cards = initialCards;
    
    // Charger les niveaux de difficulté
    try {
        const response = await fetch('/api/settings/difficulty');
        if (response.ok) {
            difficultyLevels = await response.json();
            console.log("Niveaux de difficulté chargés:", difficultyLevels);
        }
    } catch (error) {
        console.error('Erreur lors du chargement des paramètres de difficulté:', error);
    }
    
    showNextCard();
}

function formatText(text) {
    // Remplacer les sauts de ligne par des <br>
    return text.replace(/\n/g, '<br>');
}

function showNextCard() {
    if (currentCardIndex >= cards.length) {
        // Fin de la session
        console.log("Fin de la session, redirection vers:", `/decks/${deckName}`);
        window.location.href = `/decks/${deckName}`;
        return;
    }
    
    const card = cards[currentCardIndex];
    console.log("Affichage de la carte:", card);
    document.getElementById('questionText').innerHTML = formatText(card.question);
    document.getElementById('answerText').innerHTML = formatText(card.response);
    
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
    console.log("Soumission du feedback pour la carte:", card);
    console.log("Deck name:", deckName);
    
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
        const url = `/api/decks/${deckName}/cards/${card.id}/review`;
        console.log("URL de la requête:", url);
        
        const response = await fetch(url, {
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
            const errorData = await response.json();
            console.error("Erreur de la réponse:", errorData);
            alert('Erreur lors de la mise à jour de la carte');
        }
    } catch (error) {
        console.error('Erreur:', error);
        alert('Erreur lors de la mise à jour de la carte');
    }
}
