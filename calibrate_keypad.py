#!/usr/bin/env python3
"""
Script de calibration du clavier matriciel 4x4
Permet de détecter le mapping correct des touches
"""

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

row_pins = [5, 6, 13, 19]
col_pins = [12, 16, 20, 21]

# Configurer toutes les pins en INPUT PULL-UP
for pin in row_pins + col_pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("=" * 50)
print("🔧 CALIBRATION DU CLAVIER")
print("=" * 50)
print()
print("Appuyez sur chaque touche quand demandé")
print()

touches = ["1", "2", "3", "A", "4", "5", "6", "B", "7", "8", "9", "C", "*", "0", "#", "D"]
mapping = {}

for t in touches:
    print(f"Appuyez sur: [{t}]")
    found = False
    while not found:
        for r, rp in enumerate(row_pins):
            GPIO.setup(rp, GPIO.OUT)
            GPIO.output(rp, GPIO.LOW)
            time.sleep(0.002)
            for c, cp in enumerate(col_pins):
                if GPIO.input(cp) == GPIO.LOW:
                    time.sleep(0.005)
                    if GPIO.input(cp) == GPIO.LOW:
                        mapping[t] = (r, c)
                        print(f"  ✓ {t} = ROW {r}, COL {c}")
                        found = True
                        while GPIO.input(cp) == GPIO.LOW:
                            time.sleep(0.01)
                        break
            GPIO.setup(rp, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            if found:
                break
        time.sleep(0.01)
    time.sleep(0.3)

print()
print("=" * 50)
print("📋 MAPPING DÉTECTÉ")
print("=" * 50)

# Construire le nouveau layout
layout = [["?" for _ in range(4)] for _ in range(4)]
for t, (r, c) in mapping.items():
    layout[r][c] = f"'{t}'"

print()
print("Remplacez KEYS dans keypad_controller.py par :")
print()
print("KEYS = [")
for row in layout:
    print(f"    [{', '.join(row)}],")
print("]")

GPIO.cleanup()
