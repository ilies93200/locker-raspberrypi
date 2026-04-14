import time
import platform

if platform.system() != 'Windows':
    import RPi.GPIO as GPIO
    GPIO_AVAILABLE = True
else:
    GPIO_AVAILABLE = False
    print("⚠️  GPIO non disponible sur Windows - Mode simulation activé")

class LockerController:
    def __init__(self, pin=17):
        self.pin = pin
        self.is_locked = True
        self.default_open_duration = 2
        
        if GPIO_AVAILABLE:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.pin, GPIO.OUT)
            # Serrure fail-safe : HIGH = relais ON = serrure alimentée = FERMÉE
            GPIO.output(self.pin, GPIO.HIGH)
            print(f"✅ GPIO initialisé - Pin {self.pin} (serrure fail-safe, verrouillée)")
        else:
            print(f"🔧 Mode simulation - Pin {self.pin} (serrure fail-safe, verrouillée)")
    
    def ouvrir_casier(self, duree=2):
        """
        Déverrouille le casier pendant 'duree' secondes.

        Serrure fail-safe (alimentation continue) :
        - GPIO HIGH = relais ON = serrure alimentée = FERMÉE (état normal)
        - GPIO LOW  = relais OFF = serrure sans courant = OUVERTE (pendant duree secondes)
        
        Args:
            duree (int): Durée d'ouverture en secondes (défaut: 2)
        
        Returns:
            bool: True si succès, False sinon
        """
        try:
            duree = max(1, min(int(duree), 5))

            if GPIO_AVAILABLE:
                GPIO.output(self.pin, GPIO.LOW)
                print(f"🔓 Casier ouvert (GPIO {self.pin} → LOW, courant coupé, {duree}s)")
            else:
                print(f"🔓 [SIMULATION] Casier déverrouillé pendant {duree}s")
            
            self.is_locked = False
            time.sleep(duree)
            
            if GPIO_AVAILABLE:
                GPIO.output(self.pin, GPIO.HIGH)
                print(f"🔒 Casier verrouillé (GPIO {self.pin} → HIGH, serrure alimentée)")
            else:
                print(f"🔒 [SIMULATION] Casier reverrouillé")
            
            self.is_locked = True
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors de l'ouverture du casier: {e}")
            return False
    
    def verrouiller(self):
        """Force le verrouillage du casier"""
        if GPIO_AVAILABLE:
            GPIO.output(self.pin, GPIO.HIGH)
        self.is_locked = True
        print(f"🔒 Casier verrouillé (GPIO {self.pin} → HIGH)")
    
    def get_etat(self):
        """Retourne l'état actuel du casier"""
        return "verrouillé" if self.is_locked else "déverrouillé"
    
    def cleanup(self):
        """Nettoie les ressources GPIO"""
        if GPIO_AVAILABLE:
            GPIO.cleanup()
            print("🧹 GPIO nettoyé")

locker = LockerController(pin=17)
