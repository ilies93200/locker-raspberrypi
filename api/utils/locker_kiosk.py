"""
Module d'intégration clavier + casier pour le kiosk client

Ce module gère le flux complet:
1. Le client tape son code sur le clavier
2. Appuie sur # pour valider
3. Le système vérifie le code et ouvre le casier si correct
"""

import threading
from api.utils.keypad_controller import get_keypad
from api.utils.gpio_controller import locker


class LockerKiosk:
    """
    Gestionnaire du kiosk client avec clavier matriciel
    """
    
    def __init__(self, app=None):
        self.app = app
        self.keypad = None
        self.last_code = None
        self.last_result = None
        self.running = False
        
    def init_app(self, app):
        """Initialise le kiosk avec l'application Flask"""
        self.app = app
        self.keypad = get_keypad()
        self.keypad.max_buffer_length = 8  # Code de 8 caractères max
        print("✅ LockerKiosk initialisé")
    
    def start(self):
        """Démarre l'écoute du clavier"""
        if not self.keypad:
            self.keypad = get_keypad()
        
        self.running = True
        self.keypad.start(callback=self._on_code_entered)
        print("▶️ Kiosk client actif - En attente de code de retrait")
    
    def stop(self):
        """Arrête l'écoute du clavier"""
        self.running = False
        if self.keypad:
            self.keypad.stop()
        print("⏹️ Kiosk client inactif")
    
    def _on_code_entered(self, code):
        """
        Callback appelé quand un code est entré sur le clavier
        
        Args:
            code: Code entré (ou SPECIAL_X pour les touches spéciales)
        """
        if code.startswith('SPECIAL_'):
            # Gérer les touches spéciales si nécessaire
            print(f"⚡ Touche spéciale: {code}")
            return
        
        print(f"📝 Code entré: {code}")
        self.last_code = code
        
        # Valider le code avec la base de données
        result = self._validate_code(code)
        self.last_result = result
        
        if result['success']:
            print(f"✅ Code valide! Ouverture du casier...")
            locker.ouvrir_casier(duree=2)
            print(f"📦 Casier ouvert pour la commande")
        else:
            print(f"❌ Code invalide: {result['message']}")
    
    def _validate_code(self, code):
        """
        Valide un code de retrait
        
        Args:
            code: Code de retrait à valider
            
        Returns:
            dict: {'success': bool, 'message': str, 'commande': dict or None}
        """
        if not self.app:
            return {'success': False, 'message': 'Application non initialisée'}
        
        with self.app.app_context():
            from api.models import db, Commande, Casier
            from datetime import datetime
            
            # Chercher la commande par code
            commande = Commande.query.filter_by(code_commande=code).first()
            
            if not commande:
                return {'success': False, 'message': 'Code de retrait invalide'}
            
            if commande.statut != 'déposée':
                return {'success': False, 'message': 'Cette commande n\'est pas disponible'}
            
            casier = Casier.query.get(1)
            if not casier or casier.etat != 'occupé':
                return {'success': False, 'message': 'Le casier est vide'}
            
            # Tout est bon - mettre à jour le statut
            commande.statut = 'récupérée_par_client'
            commande.date_retrait = datetime.utcnow()
            casier.etat = 'libre'
            
            db.session.commit()
            
            return {
                'success': True,
                'message': 'Casier ouvert ! Récupérez votre colis.',
                'commande': commande.to_dict()
            }
    
    def get_status(self):
        """Retourne le statut actuel du kiosk"""
        return {
            'running': self.running,
            'buffer': self.keypad.get_buffer() if self.keypad else '',
            'last_code': self.last_code,
            'last_result': self.last_result
        }
    
    def clear(self):
        """Efface le buffer et les derniers résultats"""
        if self.keypad:
            self.keypad.clear_buffer()
        self.last_code = None
        self.last_result = None


# Instance globale du kiosk
kiosk = None


def init_kiosk(app):
    """Initialise l'instance globale du kiosk"""
    global kiosk
    kiosk = LockerKiosk(app)
    return kiosk


def get_kiosk():
    """Retourne l'instance globale du kiosk"""
    global kiosk
    if kiosk is None:
        kiosk = LockerKiosk()
    return kiosk
