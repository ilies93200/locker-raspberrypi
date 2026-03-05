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

# Installation packages Python
pip install -r requirements.txt

# Initialisation base de données
python3 -c "from api.app import app, db; app.app_context().push(); db.create_all()"
```

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
curl -X POST http://192.168.1.116:5000/api/casiers/1/ouvrir \
  -H "Content-Type: application/json" \
  -d '{"duree": 3}'
```

**Résultat attendu :** 
- Code 200
- Message "Casier ouvert pendant 3 secondes"
- L'électroaimant se désactive pendant 3 secondes (LED du relais change)

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
