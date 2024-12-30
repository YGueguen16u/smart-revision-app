// Fonction de suppression globale
async function deleteDeck(deckId, event) {
    // Empêche la propagation de l'événement au parent
    if (event) {
        event.preventDefault();
        event.stopPropagation();
    }

    if (!confirm('Êtes-vous sûr de vouloir supprimer ce deck ?')) {
        return;
    }

    try {
        const response = await fetch(`/api/decks/${deckId}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            // Trouve et supprime la carte du deck
            const deckCard = event.target.closest('.deck-card');
            if (deckCard) {
                deckCard.remove();
            }
        } else {
            alert('Erreur lors de la suppression du deck');
        }
    } catch (error) {
        console.error('Erreur:', error);
        alert('Erreur lors de la suppression du deck');
    }
}

// Gestion des decks
document.addEventListener('DOMContentLoaded', function() {
    const createDeckForm = document.getElementById('createDeckForm');
    if (!createDeckForm) return; // Si on n'est pas sur la page de création

    const deckNameInput = document.getElementById('deckName');

    createDeckForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const deckName = deckNameInput.value.trim();
        if (!deckName) {
            alert('Veuillez entrer un nom de deck');
            return;
        }

        try {
            const response = await fetch('/api/decks', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ name: deckName })
            });

            if (response.ok) {
                window.location.href = '/';
            } else if (response.status === 409) {
                const data = await response.json();
                const useSuggestion = confirm(
                    `${data.error}\nVoulez-vous utiliser le nom suggéré : "${data.suggestion}" ?`
                );
                
                if (useSuggestion) {
                    deckNameInput.value = data.suggestion;
                    createDeckForm.dispatchEvent(new Event('submit'));
                }
            } else {
                alert('Erreur lors de la création du deck');
            }
        } catch (error) {
            console.error('Erreur:', error);
            alert('Erreur lors de la création du deck');
        }
    });
});

function startRevision() {
    // Récupère le nom du deck depuis l'URL actuelle
    const pathParts = window.location.pathname.split('/');
    const deckName = pathParts[pathParts.length - 1];
    
    // Redirige vers la page de révision
    window.location.href = `/decks/${deckName}/review`;
}
