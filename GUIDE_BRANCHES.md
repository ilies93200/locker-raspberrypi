# Guide de Branchement - Relais actif LOW + Solénoïde 12V

## Résumé rapide

Ton branchement actuel est bon **si ton module relais CM-019 est actif LOW**.

- **GPIO HIGH** = relais coupé
- **GPIO LOW** = relais activé
- **Ouverture courte** = 2 secondes par défaut

Ça évite de laisser la serrure alimentée trop longtemps et limite l'échauffement.

---

## Branchement recommandé

### Côté Raspberry Pi

- **GPIO 17** → pin `S / IN` du relais
- **5V du Pi** → pin `+ / VCC` du relais
- **GND du Pi** → pin `- / GND` du relais

### Côté alimentation 12V / serrure

- **Alim + 12V** → **COM** du relais
- **NO** du relais → **fil rouge** de la serrure
- **fil noir** de la serrure → **Alim - 12V**

---

## Logique électrique

### Casier fermé / verrouillé

- GPIO 17 = **HIGH**
- Relais **désactivé**
- Serrure **non alimentée**

### Casier ouvert

- GPIO 17 = **LOW**
- Relais **activé**
- Serrure **alimentée** brièvement

---

## Pourquoi ça chauffe ?

Une serrure/solénoïde chauffe si :

- elle reste alimentée trop longtemps
- l'alimentation est trop forte
- la bobine est maintenue en continu au lieu d'être impulsée

### Donc il faut :

- ouvrir **1 à 3 secondes max**
- revenir à l'état repos immédiatement
- ne jamais laisser le relais activé en continu

---

## Code conseillé

```python
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT, initial=GPIO.HIGH)  # repos = relais coupé

def ouvrir_serrure():
    GPIO.output(17, GPIO.LOW)   # active le relais
    time.sleep(2)               # ouverture courte
    GPIO.output(17, GPIO.HIGH)  # coupe le relais

ouvrir_serrure()
GPIO.cleanup()
```

---

## Vérification visuelle du comportement

| État | GPIO 17 | Relais | Serrure |
|------|---------|--------|---------|
| Repos | HIGH | OFF | Non alimentée |
| Ouverture | LOW | ON | Alimentée brièvement |

---

## Point important

Si ton module est bien **actif LOW**, alors :

- **HIGH** = serrure fermée
- **LOW** = serrure ouverte

Donc le code doit être cohérent avec ça. Le câblage peut rester le même.

---

## Test rapide

```bash
ssh root@192.168.1.49 "cd ~/locker-raspberrypi && source venv/bin/activate && PYTHONPATH=/root/locker-raspberrypi python3 -c \"
from api.utils.gpio_controller import locker
locker.ouvrir_casier(2)
\""
```

---

## Recommandation pratique

- **Ne pas dépasser 2 secondes** pour la démo
- Si ça chauffe encore, réduire à **1 seconde**
- Vérifier que le relais est bien prévu pour la charge de la serrure
- Vérifier que l'alimentation 12V fournit assez de courant sans s'effondrer

---

**Conclusion :** avec ton relais CM-019, le bon réflexe est bien **GPIO HIGH au repos** et **LOW uniquement pendant une courte impulsion**.