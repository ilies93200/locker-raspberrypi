# 📖 Guide d'Installation pour le Professeur

> Installation et test du système de locker intelligent

## 🎯 Objectif

Ce guide permet d'installer et de tester rapidement le projet sur le Raspberry Pi fourni.

## ⚡ Installation Rapide (5 minutes)

### 1. Connexion au Raspberry Pi

```bash
ssh pi@192.168.1.116
# Mot de passe par défaut : raspberry (ou celui configuré)
```

### 2. Installation automatique

```bash
cd ~
git clone <url-du-depot-github> locker-project
cd locker-project
chmod +x install.sh
./install.sh
```

**OU installation manuelle :**

```bash
# Mise à jour système
sudo apt update && sudo apt upgrade -y

# Installation Python et dépendances
sudo apt install python3 python3-pip python3-venv -y

# Création environnement virtuel
python3 -m venv venv
source venv/bin/activate

# 5. Installer les dépendances Python
pip install --upgrade pip
pip install -r requirements.txt

# 6. Initialiser la base de données
python3 << 'EOF'
from api.app import app, db
from api.models import Commercant, Casier

with app.app_context():
    db.create_all()
    
    commercant = Commercant(
        id=1,
        nom='Boutique Test',
        adresse='123 Rue du Centre-Ville',
        email='boutique@test.fr',
        telephone='0123456789'
    )
    db.session.add(commercant)
    
    casier = Casier(
        id=1,
        taille='M',
        etat='libre',
        gpio_pin=17
    )
    db.session.add(casier)
    
    db.session.commit()
    print('Base de données initialisée')
EOF

# 7. Configurer le service systemd (démarrage automatique)
sudo cat > /etc/systemd/system/locker.service << 'EOF'
[Unit]
Description=Locker API Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/locker-raspberrypi
Environment=PYTHONPATH=/root/locker-raspberrypi
ExecStart=/root/locker-raspberrypi/venv/bin/python api/app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 8. Activer et démarrer le service
sudo systemctl daemon-reload
sudo systemctl enable locker.service
sudo systemctl start locker.service

# 9. Vérifier que le service fonctionne
sudo systemctl status locker.service
```

Le serveur sera accessible sur http://192.168.1.116:5000

**Note :** Le service démarre automatiquement au démarrage du Raspberry Pi.

### 3. Configuration Email (optionnel pour les tests)

Créer le fichier `.env` :

```bash
nano .env
```

Contenu :
```
SMTP_USERNAME=email-test@gmail.com
SMTP_PASSWORD=mot-de-passe-application
```

### 4. Lancement du serveur

```bash
source venv/bin/activate
python api/app.py
```

Le serveur démarre sur `http://192.168.1.116:5000`

## 🧪 Tests Fonctionnels

### Test 1 : Accès aux interfaces

Depuis un navigateur sur le réseau local :

1. **Page d'accueil** : http://192.168.1.116:5000
2. **Interface Commerçant** : http://192.168.1.116:5000/commercant
3. **Interface Livreur** : http://192.168.1.116:5000/livreur
4. **Interface Client** : http://192.168.1.116:5000/client

### Test 2 : Création d'un livreur (API)

```bash
curl -X POST http://192.168.1.116:5000/api/livreurs \
  -H "Content-Type: application/json" \
  -d '{
    "nom": "Dupont",
    "prenom": "Jean",
    "login": "jdupont",
    "password": "test123",
    "adresse": "123 Rue Test"
  }'
```

**Résultat attendu :** Code 201 + JSON du livreur créé

### Test 3 : Connexion livreur

```bash
curl -X POST http://192.168.1.116:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "login": "jdupont",
    "password": "test123"
  }'
```

**Résultat attendu :** Code 200 + token JWT + `first_login: true`

### Test 4 : Création d'une commande

```bash
curl -X POST http://192.168.1.116:5000/api/commandes \
  -H "Content-Type: application/json" \
  -d '{
    "email_client": "client@test.fr",
    "taille_casier": "M",
    "poids": 2.5,
    "commercant_id": 1
  }'
```

**Résultat attendu :** Code 201 + JSON de la commande

### Test 5 : État du casier

```bash
curl http://192.168.1.116:5000/api/casiers
```

**Résultat attendu :** 
```json
{
  "id": 1,
  "taille": "M",
  "etat": "libre",
  "gpio_pin": 17
}
```

### Test 6 : Ouverture du casier (test GPIO)

```bash
curl -X POST http://192.168.1.116:5000/api/casiers/1/ouvrir
```

**Résultat attendu :** Le casier s'ouvre pendant 5 secondes

### Commandes Utiles

```bash
# Voir les logs en temps réel
sudo journalctl -u locker.service -f

# Redémarrer le service
sudo systemctl restart locker.service

# Arrêter le service
sudo systemctl stop locker.service

# Vérifier l'état de la base de données
cd ~/locker-raspberrypi
sqlite3 instance/locker.db "SELECT * FROM casier;"
sqlite3 instance/locker.db "SELECT * FROM commercants;"
sqlite3 instance/locker.db "SELECT * FROM livreurs;"
sqlite3 instance/locker.db "SELECT * FROM commandes;"
```

## 🔌 Vérification du Câblage GPIO

### Schéma de connexion

```
Raspberry Pi          Module Relais          Électroaimant
────────────          ─────────────          ─────────────
GPIO 17 (Pin 11) ──> IN
GND (Pin 6)      ──> GND
5V (Pin 2)       ──> VCC
                      COM ───────────────> + 12V
                      NO  ───────────────> Électroaimant +
                                           Électroaimant - ──> GND 12V
```

### Test manuel GPIO (sans API)

```bash
python3 << EOF
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

print("Verrouillage (HIGH)...")
GPIO.output(17, GPIO.HIGH)
time.sleep(2)

print("Déverrouillage (LOW)...")
GPIO.output(17, GPIO.LOW)
time.sleep(3)

print("Reverrouillage (HIGH)...")
GPIO.output(17, GPIO.HIGH)

GPIO.cleanup()
print("Test terminé")
EOF
```

## 📊 Vérification de la Base de Données

```bash
sqlite3 locker.db

# Commandes SQL utiles :
.tables                          # Lister les tables
SELECT * FROM livreurs;          # Voir les livreurs
SELECT * FROM commandes;         # Voir les commandes
SELECT * FROM casier;            # Voir l'état du casier
.quit                            # Quitter
```

## 🎬 Scénario Complet de Test

### Étape 1 : Créer un livreur (Commerçant)

Via l'interface web `http://192.168.1.116:5000/commercant` :
1. Aller dans "Livreurs"
2. Créer : Jean Dupont, login: `jdupont`, mdp: `test123`

### Étape 2 : Créer une commande (Commerçant)

1. Aller dans "Commandes"
2. Créer une commande :
   - Email client : `test@example.com`
   - Taille : M
   - Poids : 2kg

### Étape 3 : Connexion livreur

Via `http://192.168.1.116:5000/livreur` :
1. Login : `jdupont`
2. Mot de passe : `test123`
3. Changer le mot de passe (premier login)

### Étape 4 : Récupération commande (Livreur)

1. Voir la commande disponible
2. Cliquer "Récupérer chez le commerçant"

### Étape 5 : Dépôt dans le casier (Livreur)

1. Cliquer "Déposer dans le casier"
2. Le casier s'ouvre automatiquement (GPIO)
3. Un email est envoyé au client avec code + mot de passe

### Étape 6 : Retrait client

Via `http://192.168.1.116:5000/client` :
1. Entrer le code de commande (ex: `CMD-20240312-0042`)
2. Entrer le mot de passe (ex: `7K3mP9`)
3. Le casier s'ouvre

## ⚠️ Problèmes Courants

### Le serveur ne démarre pas

```bash
# Vérifier que le port 5000 est libre
sudo lsof -i :5000

# Si occupé, tuer le processus
sudo kill -9 <PID>
```

### GPIO ne fonctionne pas

```bash
# Vérifier les permissions
sudo usermod -a -G gpio pi
sudo reboot
```

### Email ne s'envoie pas

Mode simulation activé par défaut. Les codes sont affichés dans les logs du serveur.

## 📝 Notes pour l'Évaluation

- **Code source** : Bien structuré, commenté, suit les bonnes pratiques Python
- **Base de données** : Schéma normalisé, contraintes d'intégrité
- **API REST** : Endpoints cohérents, gestion d'erreurs
- **Interfaces web** : Responsive, ergonomiques
- **GPIO** : Contrôle fonctionnel de l'électroaimant
- **Documentation** : Complète (README, PROJET_LOCKER.md, ce guide)

## 📞 Support

En cas de problème lors de l'installation, vérifier :
1. Les logs du serveur Flask
2. La connexion réseau (ping 192.168.1.116)
3. Les permissions GPIO
4. La version de Python (3.7+)

---

**Temps d'installation estimé :** 5-10 minutes  
**Temps de test complet :** 15-20 minutes
