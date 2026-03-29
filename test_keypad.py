#!/usr/bin/env python3
"""
Script de test pour le clavier matriciel 4x4

CÂBLAGE À VÉRIFIER:
==================

Le clavier a 8 broches:
- 4 pour les RANGÉES (ROW)
- 4 pour les COLONNES (COL)

Brochage par défaut dans le code:
- ROW (Rangées): GPIO 5, 6, 13, 19
- COL (Colonnes): GPIO 12, 16, 20, 21

Si ton clavier est différent, tu peux modifier les pins ci-dessous.
"""

import sys
import os

# Ajouter le chemin du projet
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api.utils.keypad_controller import KeypadController
import time

def test_keypad():
    print("=" * 50)
    print("🧪 TEST DU CLAVIER MATRICIEL 4x4")
    print("=" * 50)
    print()
    print("CÂBLAGE PAR DÉFAUT:")
    print("  Rangées (ROW): GPIO 5, 6, 13, 19")
    print("  Colonnes (COL): GPIO 12, 16, 20, 21")
    print()
    print("LAYOUT:")
    print("  [1] [2] [3] [A]")
    print("  [4] [5] [6] [B]")
    print("  [7] [8] [9] [C]")
    print("  [*] [0] [#] [D]")
    print()
    print("-" * 50)
    print("INSTRUCTIONS:")
    print("  - Appuyez sur les touches pour tester")
    print("  - [*] = Effacer le buffer")
    print("  - [#] = Valider le code")
    print("  - Ctrl+C pour quitter")
    print("-" * 50)
    print()
    
    # Tu peux modifier ces pins selon ton câblage
    # Exemple: row_pins=[2, 3, 4, 17], col_pins=[22, 23, 24, 27]
    keypad = KeypadController()
    
    def on_key(code):
        if code.startswith('SPECIAL_'):
            print(f"⚡ Touche spéciale: {code}")
        else:
            print(f"✅ CODE COMPLET: {code}")
            print(f"   Longueur: {len(code)} caractères")
    
    keypad.start(callback=on_key)
    
    try:
        while True:
            buffer = keypad.get_buffer()
            if buffer:
                print(f"\r📝 Buffer actuel: {buffer}    ", end="", flush=True)
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n\n⏹️ Test terminé")
        keypad.cleanup()


def test_pins():
    """Teste chaque pin individuellement pour vérifier le câblage"""
    print("=" * 50)
    print("🔧 TEST DES PINS GPIO")
    print("=" * 50)
    
    try:
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)
        
        row_pins = [5, 6, 13, 19]
        col_pins = [12, 16, 20, 21]
        
        print("\nConfiguration des rangées (OUTPUT):")
        for pin in row_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.HIGH)
            print(f"  GPIO {pin}: OUTPUT HIGH ✓")
        
        print("\nConfiguration des colonnes (INPUT PULL-UP):")
        for pin in col_pins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            state = GPIO.input(pin)
            print(f"  GPIO {pin}: INPUT (état: {'HIGH' if state else 'LOW'}) ✓")
        
        print("\n✅ Pins configurées correctement!")
        print("\nMaintenant, appuyez sur une touche du clavier...")
        
        # Test simple de détection
        while True:
            for row_idx, row_pin in enumerate(row_pins):
                GPIO.output(row_pin, GPIO.LOW)
                
                for col_idx, col_pin in enumerate(col_pins):
                    if GPIO.input(col_pin) == GPIO.LOW:
                        keys = [
                            ['1', '2', '3', 'A'],
                            ['4', '5', '6', 'B'],
                            ['7', '8', '9', 'C'],
                            ['*', '0', '#', 'D']
                        ]
                        key = keys[row_idx][col_idx]
                        print(f"🔘 Touche détectée: {key} (ROW {row_idx}, COL {col_idx})")
                        time.sleep(0.3)
                
                GPIO.output(row_pin, GPIO.HIGH)
            
            time.sleep(0.01)
            
    except KeyboardInterrupt:
        print("\n\n⏹️ Test terminé")
        GPIO.cleanup()
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        print("\nSi tu es sur Windows, ce test ne peut pas fonctionner.")
        print("Exécute ce script directement sur le Raspberry Pi.")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test du clavier matriciel")
    parser.add_argument('--pins', action='store_true', help="Tester les pins GPIO individuellement")
    args = parser.parse_args()
    
    if args.pins:
        test_pins()
    else:
        test_keypad()
