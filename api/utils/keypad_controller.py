import time
import platform
import threading

if platform.system() != 'Windows':
    import RPi.GPIO as GPIO
    GPIO_AVAILABLE = True
else:
    GPIO_AVAILABLE = False
    print("⚠️  GPIO non disponible sur Windows - Mode simulation clavier activé")


class KeypadController:
    """
    Contrôleur pour clavier matriciel 4x4 (8 broches)
    
    Brochage typique:
    - Rangées (ROW): GPIO 5, 6, 13, 19 (sorties)
    - Colonnes (COL): GPIO 12, 16, 20, 21 (entrées avec pull-up)
    
    Layout standard:
        [1] [2] [3] [A]
        [4] [5] [6] [B]
        [7] [8] [9] [C]
        [*] [0] [#] [D]
    """
    
    # Layout du clavier 4x4
    KEYS = [
        ['1', '2', '3', 'A'],
        ['4', '5', '6', 'B'],
        ['7', '8', '9', 'C'],
        ['*', '0', '#', 'D']
    ]
    
    def __init__(self, row_pins=None, col_pins=None):
        """
        Initialise le clavier matriciel
        
        Args:
            row_pins: Liste des pins GPIO pour les rangées (défaut: [5, 6, 13, 19])
            col_pins: Liste des pins GPIO pour les colonnes (défaut: [12, 16, 20, 21])
        """
        # Pins selon ton câblage (GPIO 17 = relais, donc on utilise d'autres pins)
        self.row_pins = row_pins or [5, 6, 13, 19]
        self.col_pins = col_pins or [12, 16, 20, 21]
        
        self.buffer = ""
        self.max_buffer_length = 8
        self.callback = None
        self.running = False
        self.scan_thread = None
        
        if GPIO_AVAILABLE:
            self._setup_gpio()
            print(f"✅ Clavier initialisé - Rangées: {self.row_pins}, Colonnes: {self.col_pins}")
        else:
            print(f"🔧 Mode simulation - Clavier 4x4")
    
    def _setup_gpio(self):
        """Configure les GPIO pour le clavier matriciel"""
        GPIO.setmode(GPIO.BCM)
        
        # Configurer les rangées en sortie (HIGH par défaut)
        for pin in self.row_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.HIGH)
        
        # Configurer les colonnes en entrée avec pull-up
        for pin in self.col_pins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    def _scan_keypad(self):
        """
        Scanne le clavier pour détecter une touche pressée
        Retourne la touche pressée ou None
        """
        if not GPIO_AVAILABLE:
            return None
        
        for row_idx, row_pin in enumerate(self.row_pins):
            # Mettre la rangée à LOW
            GPIO.output(row_pin, GPIO.LOW)
            
            # Vérifier chaque colonne
            for col_idx, col_pin in enumerate(self.col_pins):
                if GPIO.input(col_pin) == GPIO.LOW:
                    # Touche détectée!
                    key = self.KEYS[row_idx][col_idx]
                    
                    # Attendre que la touche soit relâchée (debounce)
                    time.sleep(0.05)
                    while GPIO.input(col_pin) == GPIO.LOW:
                        time.sleep(0.01)
                    
                    # Remettre la rangée à HIGH
                    GPIO.output(row_pin, GPIO.HIGH)
                    return key
            
            # Remettre la rangée à HIGH
            GPIO.output(row_pin, GPIO.HIGH)
        
        return None
    
    def _scan_loop(self):
        """Boucle de scan en arrière-plan"""
        last_key = None
        debounce_time = 0.3
        last_press_time = 0
        
        while self.running:
            key = self._scan_keypad()
            
            if key and key != last_key:
                current_time = time.time()
                if current_time - last_press_time > debounce_time:
                    self._handle_key_press(key)
                    last_press_time = current_time
                    last_key = key
            elif not key:
                last_key = None
            
            time.sleep(0.01)
    
    def _handle_key_press(self, key):
        """Gère une touche pressée"""
        print(f"🔘 Touche pressée: {key}")
        
        if key == '*':
            # Effacer le buffer
            self.buffer = ""
            print("🗑️ Buffer effacé")
        elif key == '#':
            # Valider le code
            if self.callback:
                self.callback(self.buffer)
        elif key in ['A', 'B', 'C', 'D']:
            # Touches spéciales - peut être utilisé pour d'autres actions
            if self.callback:
                self.callback(f"SPECIAL_{key}")
        else:
            # Ajouter au buffer
            if len(self.buffer) < self.max_buffer_length:
                self.buffer += key
                print(f"📝 Buffer: {self.buffer}")
    
    def start(self, callback=None):
        """
        Démarre la lecture du clavier en arrière-plan
        
        Args:
            callback: Fonction appelée quand un code est validé (touche #)
                     ou une touche spéciale est pressée
        """
        self.callback = callback
        self.running = True
        self.scan_thread = threading.Thread(target=self._scan_loop, daemon=True)
        self.scan_thread.start()
        print("▶️ Lecture du clavier démarrée")
    
    def stop(self):
        """Arrête la lecture du clavier"""
        self.running = False
        if self.scan_thread:
            self.scan_thread.join(timeout=1)
        print("⏹️ Lecture du clavier arrêtée")
    
    def get_buffer(self):
        """Retourne le buffer actuel"""
        return self.buffer
    
    def clear_buffer(self):
        """Efface le buffer"""
        self.buffer = ""
    
    def set_buffer(self, value):
        """Définit le buffer"""
        self.buffer = str(value)[:self.max_buffer_length]
    
    def wait_for_code(self, timeout=30):
        """
        Attend un code complet (bloquant)
        
        Args:
            timeout: Temps maximum d'attente en secondes
        
        Returns:
            str: Code entré ou None si timeout
        """
        result = {'code': None}
        event = threading.Event()
        
        def on_code(code):
            if not code.startswith('SPECIAL_'):
                result['code'] = code
                event.set()
        
        self.start(callback=on_code)
        event.wait(timeout=timeout)
        self.stop()
        
        return result['code']
    
    def cleanup(self):
        """Nettoie les ressources GPIO"""
        self.stop()
        if GPIO_AVAILABLE:
            # Ne pas cleanup tous les GPIO, seulement ceux du clavier
            for pin in self.row_pins + self.col_pins:
                GPIO.setup(pin, GPIO.IN)
            print("🧹 GPIO clavier nettoyé")


# Instance globale du clavier
keypad = None


def init_keypad(row_pins=None, col_pins=None):
    """Initialise l'instance globale du clavier"""
    global keypad
    keypad = KeypadController(row_pins, col_pins)
    return keypad


def get_keypad():
    """Retourne l'instance globale du clavier"""
    global keypad
    if keypad is None:
        keypad = KeypadController()
    return keypad


# Test du clavier
if __name__ == "__main__":
    print("🧪 Test du clavier matriciel 4x4")
    print("Appuyez sur les touches pour tester. Ctrl+C pour quitter.")
    
    def on_key(code):
        if code.startswith('SPECIAL_'):
            print(f"⚡ Touche spéciale: {code}")
        else:
            print(f"✅ Code validé: {code}")
    
    keypad = get_keypad()
    keypad.start(callback=on_key)
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n⏹️ Arrêt du test")
        keypad.cleanup()
