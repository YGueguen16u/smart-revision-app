class DifficultySettings {
    constructor() {
        this.container = document.getElementById('difficulty-settings');
        this.levels = ['very_hard', 'hard', 'medium', 'easy', 'very_easy'];
        this.minDifference = 60; // Différence minimale en minutes (1 heure)
        this.minValue = 1;
        this.timeUnits = {
            'minutes': 1,
            'heures': 60,
            'jours': 1440
        };
        this.initializePanel();
    }

    initializePanel() {
        const overlay = document.createElement('div');
        overlay.className = 'settings-overlay';
        overlay.id = 'settings-overlay';

        const unitOptions = Object.keys(this.timeUnits)
            .map(unit => `<option value="${unit}">${unit}</option>`)
            .join('');

        overlay.innerHTML = `
            <div class="difficulty-settings">
                <button class="settings-close" onclick="toggleSettings()">×</button>
                <h2 class="difficulty-title">Paramètres de difficulté</h2>
                <form id="difficulty-form" class="difficulty-grid">
                    <div class="difficulty-row">
                        <label class="difficulty-label" for="very_hard">Très difficile</label>
                        <div class="input-unit-group">
                            <input type="number" class="difficulty-input" id="very_hard" name="very_hard" min="1" required>
                            <select class="unit-select" id="very_hard_unit">${unitOptions}</select>
                        </div>
                    </div>
                    <div class="difficulty-row">
                        <label class="difficulty-label" for="hard">Difficile</label>
                        <div class="input-unit-group">
                            <input type="number" class="difficulty-input" id="hard" name="hard" min="1" required>
                            <select class="unit-select" id="hard_unit">${unitOptions}</select>
                        </div>
                    </div>
                    <div class="difficulty-row">
                        <label class="difficulty-label" for="medium">Moyen</label>
                        <div class="input-unit-group">
                            <input type="number" class="difficulty-input" id="medium" name="medium" min="1" required>
                            <select class="unit-select" id="medium_unit">${unitOptions}</select>
                        </div>
                    </div>
                    <div class="difficulty-row">
                        <label class="difficulty-label" for="easy">Facile</label>
                        <div class="input-unit-group">
                            <input type="number" class="difficulty-input" id="easy" name="easy" min="1" required>
                            <select class="unit-select" id="easy_unit">${unitOptions}</select>
                        </div>
                    </div>
                    <div class="difficulty-row">
                        <label class="difficulty-label" for="very_easy">Très facile</label>
                        <div class="input-unit-group">
                            <input type="number" class="difficulty-input" id="very_easy" name="very_easy" min="1" required>
                            <select class="unit-select" id="very_easy_unit">${unitOptions}</select>
                        </div>
                    </div>
                    <button type="submit" class="submit-button">Enregistrer</button>
                </form>
            </div>
        `;

        document.body.appendChild(overlay);
        
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) {
                toggleSettings();
            }
        });

        const form = document.getElementById('difficulty-form');
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.saveSettings();
        });

        this.levels.forEach((level, index) => {
            const input = document.getElementById(level);
            const unitSelect = document.getElementById(`${level}_unit`);
            
            input.addEventListener('input', (e) => {
                const value = parseInt(e.target.value);
                if (value < this.minValue) {
                    e.target.value = this.minValue;
                }
                this.validateAndAdjustValues(index);
            });

            unitSelect.addEventListener('change', () => {
                this.validateAndAdjustValues(index);
            });
        });

        this.loadSettings();
    }

    getValueInMinutes(level) {
        const input = document.getElementById(level);
        const unitSelect = document.getElementById(`${level}_unit`);
        const value = parseInt(input.value) || 0;
        const unit = unitSelect.value;
        return value * this.timeUnits[unit];
    }

    getMinDifferenceForUnit(unit) {
        switch(unit) {
            case 'jours':
                return 1; // 1 jour de différence minimum
            case 'heures':
                return 2; // 2 heures de différence minimum
            default:
                return 60; // 60 minutes de différence minimum
        }
    }

    setValueFromMinutes(level, minutes) {
        const input = document.getElementById(level);
        const unitSelect = document.getElementById(`${level}_unit`);
        let value = minutes;
        let unit = 'minutes';

        if (minutes >= 1440) {
            value = Math.floor(minutes / 1440);
            unit = 'jours';
        } else if (minutes >= 60) {
            value = Math.floor(minutes / 60);
            unit = 'heures';
        }

        input.value = Math.max(1, value);
        unitSelect.value = unit;
    }

    validateAndAdjustValues(changedIndex) {
        const values = this.levels.map(level => this.getValueInMinutes(level));
        
        // Vérifier et ajuster les valeurs vers le haut (du plus difficile au plus facile)
        for (let i = changedIndex - 1; i >= 0; i--) {
            const currentMinutes = values[i];
            const nextMinutes = values[i + 1];
            const currentUnit = document.getElementById(`${this.levels[i]}_unit`).value;
            const minDiff = this.getMinDifferenceForUnit(currentUnit) * this.timeUnits[currentUnit];
            
            if (currentMinutes >= nextMinutes - minDiff) {
                values[i] = Math.max(this.minValue, nextMinutes - minDiff);
            }
        }

        // Vérifier et ajuster les valeurs vers le bas (du plus facile au plus difficile)
        for (let i = changedIndex + 1; i < values.length; i++) {
            const currentMinutes = values[i];
            const prevMinutes = values[i - 1];
            const currentUnit = document.getElementById(`${this.levels[i]}_unit`).value;
            const minDiff = this.getMinDifferenceForUnit(currentUnit) * this.timeUnits[currentUnit];
            
            if (currentMinutes <= prevMinutes + minDiff) {
                values[i] = prevMinutes + minDiff;
            }
        }

        // Mettre à jour tous les champs avec les nouvelles valeurs
        values.forEach((minutes, index) => {
            this.setValueFromMinutes(this.levels[index], minutes);
        });
    }

    loadSettings() {
        fetch('/api/settings/difficulty')
            .then(response => response.json())
            .then(data => {
                this.levels.forEach(level => {
                    if (data[level]) {
                        this.setValueFromMinutes(level, data[level]);
                    }
                });
            })
            .catch(error => {
                console.error('Erreur lors du chargement des paramètres:', error);
                this.showAlert('danger', 'Erreur lors du chargement des paramètres');
            });
    }

    saveSettings() {
        const settings = {};
        this.levels.forEach(level => {
            settings[level] = this.getValueInMinutes(level);
        });

        if (!this.validateSettings(settings)) {
            this.showAlert('danger', 'Les temps doivent être croissants du niveau très difficile au niveau très facile');
            return;
        }

        fetch('/api/settings/difficulty', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(settings)
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                this.showAlert('danger', data.error);
            } else {
                this.showAlert('success', 'Paramètres enregistrés avec succès');
                setTimeout(() => toggleSettings(), 1500);
            }
        })
        .catch(error => {
            console.error('Erreur lors de la sauvegarde:', error);
            this.showAlert('danger', 'Erreur lors de la sauvegarde des paramètres');
        });
    }

    validateSettings(settings) {
        if (settings[this.levels[0]] < this.minValue) return false;
        
        for (let i = 0; i < this.levels.length - 1; i++) {
            if (settings[this.levels[i]] >= settings[this.levels[i + 1]]) {
                return false;
            }
        }
        return true;
    }

    showAlert(type, message) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type}`;
        alertDiv.textContent = message;

        const settingsDiv = document.querySelector('.difficulty-settings');
        settingsDiv.insertBefore(alertDiv, settingsDiv.firstChild);

        setTimeout(() => alertDiv.remove(), 5000);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new DifficultySettings();
});