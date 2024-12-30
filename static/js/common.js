// Fonction pour basculer l'affichage des paramètres
window.toggleSettings = function() {
    const overlay = document.getElementById('settings-overlay');
    if (overlay) {
        if (overlay.style.display === 'flex') {
            overlay.style.opacity = '0';
            setTimeout(() => {
                overlay.style.display = 'none';
                overlay.style.opacity = '1';
            }, 300);
        } else {
            overlay.style.display = 'flex';
        }
    }
};

// Fonction pour basculer l'affichage des paramètres
window.toggleSettings = function() {
    const overlay = document.getElementById('settings-overlay');
    if (overlay) {
        if (overlay.style.display === 'flex') {
            overlay.style.opacity = '0';
            setTimeout(() => {
                overlay.style.display = 'none';
                overlay.style.opacity = '1';
            }, 300);
        } else {
            overlay.style.display = 'flex';
        }
    }
};

// Initialiser le panneau de paramètres au chargement de la page
document.addEventListener('DOMContentLoaded', () => {
    // Créer le panneau de paramètres s'il n'existe pas déjà
    if (!document.getElementById('settings-overlay')) {
        const overlay = document.createElement('div');
        overlay.className = 'settings-overlay';
        overlay.id = 'settings-overlay';
        overlay.style.display = 'none';
        document.body.appendChild(overlay);
    }
});