from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json

class RevisionTask:
    def __init__(self, name: str, dependencies: List[str] = None):
        self.name = name
        self.dependencies = dependencies or []
        self.completed = False
        self.next_revision = None
        self.difficulty_factor = 2.5  # Facteur initial de difficulté
        self.consecutive_correct = 0

    def mark_completed(self, quality: int):
        """
        Marque une tâche comme complétée et planifie la prochaine révision
        quality: Note de 0 à 5 sur la qualité de la réponse
        """
        self.completed = True
        
        # Algorithme SM-2 modifié
        if quality >= 3:
            if self.consecutive_correct == 0:
                interval = timedelta(days=1)
            elif self.consecutive_correct == 1:
                interval = timedelta(days=3)
            else:
                interval = timedelta(days=int(self.consecutive_correct * self.difficulty_factor))
            
            self.consecutive_correct += 1
            self.difficulty_factor += 0.1
        else:
            self.consecutive_correct = 0
            self.difficulty_factor = max(1.3, self.difficulty_factor - 0.2)
            interval = timedelta(minutes=30)

        self.next_revision = datetime.now() + interval

class RevisionFlow:
    def __init__(self):
        self.tasks: Dict[str, RevisionTask] = {}
        self.current_session = []
        
    def add_task(self, name: str, dependencies: List[str] = None):
        """Ajoute une nouvelle tâche au flux de révision"""
        if name in self.tasks:
            raise ValueError(f"La tâche {name} existe déjà")
            
        for dep in (dependencies or []):
            if dep not in self.tasks:
                raise ValueError(f"La dépendance {dep} n'existe pas")
                
        self.tasks[name] = RevisionTask(name, dependencies)
        
    def get_available_tasks(self) -> List[RevisionTask]:
        """Retourne les tâches disponibles pour révision"""
        now = datetime.now()
        available = []
        
        for task in self.tasks.values():
            if task.next_revision and task.next_revision > now:
                continue
                
            if all(self.tasks[dep].completed for dep in task.dependencies):
                available.append(task)
                
        return available
        
    def start_session(self, duration: timedelta = timedelta(minutes=30)):
        """Démarre une session de révision"""
        self.current_session = self.get_available_tasks()
        self.session_end = datetime.now() + duration
        
    def get_next_task(self) -> Optional[RevisionTask]:
        """Retourne la prochaine tâche à réviser"""
        if not self.current_session or datetime.now() > self.session_end:
            return None
            
        return self.current_session.pop(0)
        
    def save_state(self, filename: str):
        """Sauvegarde l'état du flux de révision"""
        state = {
            name: {
                'completed': task.completed,
                'next_revision': task.next_revision.isoformat() if task.next_revision else None,
                'difficulty_factor': task.difficulty_factor,
                'consecutive_correct': task.consecutive_correct,
                'dependencies': task.dependencies
            }
            for name, task in self.tasks.items()
        }
        
        with open(filename, 'w') as f:
            json.dump(state, f)
            
    def load_state(self, filename: str):
        """Charge l'état du flux de révision"""
        with open(filename, 'r') as f:
            state = json.load(f)
            
        self.tasks.clear()
        for name, data in state.items():
            task = RevisionTask(name, data['dependencies'])
            task.completed = data['completed']
            task.next_revision = datetime.fromisoformat(data['next_revision']) if data['next_revision'] else None
            task.difficulty_factor = data['difficulty_factor']
            task.consecutive_correct = data['consecutive_correct']
            self.tasks[name] = task

# Exemple d'utilisation
if __name__ == '__main__':
    flow = RevisionFlow()
    
    # Création d'un flux de révision pour les mathématiques
    flow.add_task("Bases d'algèbre")
    flow.add_task("Équations du premier degré", ["Bases d'algèbre"])
    flow.add_task("Équations du second degré", ["Équations du premier degré"])
    flow.add_task("Systèmes d'équations", ["Équations du premier degré"])
    
    # Démarrage d'une session
    flow.start_session(timedelta(minutes=45))
    
    # Simulation d'une session de révision
    while task := flow.get_next_task():
        # Simuler une révision
        quality = 4  # Qualité de la réponse (0-5)
        task.mark_completed(quality)
        
    # Sauvegarde de l'état
    flow.save_state("revision_state.json")
