# 📦 Projet Locker de Livraison — Plan Complet

> Projet BTS/Lycée — Système de casiers intelligents pour commerçants piétons  
> Raspberry Pi : `192.168.1.116`

---

## 1. Compréhension du Projet

### 1.1 Contexte

Des commerçants d'un centre-ville piéton veulent mettre en place des **casiers de livraison** (lockers) pour leurs clients. Raisons :
- Certains clients ne peuvent pas venir en horaires d'ouverture
- D'autres préfèrent récupérer leur colis dans la journée plutôt qu'attendre une livraison classique
- D'autres veulent continuer à flâner sans porter des sacs

Le locker est placé sur le **parking du centre-ville**. Un écran tactile sur l'armoire permet aux clients de récupérer leur commande.

---

### 1.2 Les 3 Acteurs du Système

| Acteur | Rôle |
|--------|------|
| **Commerçant** | Saisit les commandes, crée les profils livreurs, suit l'état des casiers |
| **Livreur** | S'authentifie, voit les commandes, dépose les colis dans les casiers |
| **Client** | Reçoit un mail avec code commande + mot de passe, va au locker et entre les codes pour ouvrir son casier |

---

### 1.3 Schéma d'Architecture

```
    RÉSEAU LOCAL (192.168.1.x)
    
┌─────────────────────┐        ┌──────────────────────────┐
│   IHM Commerçant    │        │    App Livreur           │
│  (Navigateur Web)   │        │  (Navigateur Web)        │
│  PC ou Tablette     │        │  Téléphone ou Tablette   │
│                     │        │                          │
│  - Créer livreurs   │        │  - S'authentifier        │
│  - Saisir commandes │        │  - Voir commandes dispo  │
│  - Voir état casiers│        │  - Valider récupération  │
│  - Supprimer cmds   │        │  - Ouvrir casier         │
└────────┬────────────┘        └──────────┬───────────────┘
         │                               │
         │ http://192.168.1.116:5000     │ http://192.168.1.116:5000
         │                               │
         └──────────────┬────────────────┘
                        │
               ┌────────▼─────────────────────────────────┐
               │   🍓 RASPBERRY PI (192.168.1.116)        │
               │   ════════════════════════════════════   │
               │                                          │
               │  ┌────────────────────────────────────┐  │
               │  │   Flask Web Server (port 5000)     │  │
               │  │   • API REST                       │  │
               │  │   • Pages Web (HTML/CSS/JS)        │  │
               │  └────────────────────────────────────┘  │
               │  ┌────────────────────────────────────┐  │
               │  │   Base de données SQLite           │  │
               │  │   (locker.db)                      │  │
               │  └────────────────────────────────────┘  │
               │  ┌────────────────────────────────────┐  │
               │  │   Interface Client Kiosk           │  │
               │  │   (Écran tactile — Chromium)       │  │
               │  │   http://localhost:5000/client     │  │
               │  └────────────────────────────────────┘  │
               │  ┌────────────────────────────────────┐  │
               │  │   Contrôleur GPIO (RPi.GPIO)       │  │
               │  │   • Module relais 4 canaux         │  │
               │  │   • Électroaimants (1 par casier)  │  │
               │  │   GPIO 17, 18, 27, 22              │  │
               │  └────────────────────────────────────┘  │
               │  ┌────────────────────────────────────┐  │
               │  │   Envoi Email (smtplib)            │  │
               │  │   Gmail SMTP                       │  │
               │  └────────────────────────────────────┘  │
               └──────────────────────────────────────────┘
                        │
                        │ SMTP (Gmail)
                        ▼
               ┌─────────────────┐
               │  📧 Email Client │
               │  code commande  │
               │  + mot de passe │
               └─────────────────┘
```

> **💡 Architecture 100% locale** :
> - Tout tourne sur le Raspberry Pi (serveur web + BDD + GPIO)
> - Pas besoin d'hébergement externe
> - Accès via `http://192.168.1.116:5000` depuis n'importe quel appareil du réseau local
> - L'application Android est **remplacée** par une **web app** (zéro installation)

---

## 2. Répartition des Fonctions (selon le sujet)

### Étudiant 1 — IHM Commerçant (Application Windows → ici Web App)

- [x] Créer un profil livreur (nom, prénom, adresse, login, mot de passe temporaire)
- [x] Saisir une commande (mail client, taille de casier, poids colis, nom/adresse commerçant)
- [x] Certifier la récupération d'un colis par un livreur (sélection parmi disponibles)
- [x] Afficher l'état de chaque casier
- [x] Supprimer une commande non récupérée
- [x] Toutes les interactions via la **BDD**

### Étudiant 2 — App Livreur (Android → ici Web App)

- [x] Connexion sécurisée (premier login = forcer changement de mot de passe)
- [x] Valider la récupération d'une commande auprès d'un commerçant
- [x] Ouvrir un casier vide correspondant à la taille du colis
- [x] Valider la livraison dans le casier
- [x] Afficher toutes les commandes récupérables chez les commerçants + adresses
- [x] Interactions avec la **BDD**

### Étudiant 3 — Raspberry Pi + Interface Client + Locker

- [x] Interface permettant d'entrer un numéro de commande et un mot de passe
  - Message si numéro de commande inexistant
  - Message si mot de passe incorrect
  - Message de succès + ouverture du casier correspondant
- [x] Envoi automatique d'un mail (numéro de commande + mot de passe généré) quand la commande est disponible au locker
- [x] Création d'une **API REST** pour que l'app livreur interagisse avec le locker
- [x] Création de la maquette physique (Raspberry Pi + électroaimants)
- [x] Interactions avec la **BDD**

### Commun (tous)

- [ ] Diagramme SysML du système complet
- [ ] Implantation de la BDD sur le serveur (ici le Raspberry Pi)
- [ ] Intégration et mise en commun des solutions
- [ ] Tests finaux de fonctionnement de l'installation complète

---

## 3. Matériel Électronique Nécessaire

### 3.1 Liste du Matériel

| Composant | Quantité | Description | Exemple |
|-----------|----------|-------------|---------|
| **Raspberry Pi** | 1 | Modèle 3B+, 4 ou 5 avec WiFi | Raspberry Pi 4 (2GB RAM minimum) |
| **Carte microSD** | 1 | 32GB minimum | SanDisk Ultra 32GB |
| **Module relais** | 1 | 1 canal, 5V, compatible GPIO | Module relais 1 canal SRD-05VDC |
| **Électroaimant** | 1 | 12V, force de maintien ~5kg | Électroaimant 12V 2.5kg |
| **Alimentation 12V** | 1 | Pour les électroaimants (min 2A) | Adaptateur 12V 3A |
| **Écran tactile** | 1 | 7" HDMI pour interface client | Écran tactile Raspberry Pi officiel |
| **Câbles Dupont** | 1 lot | Femelle-Femelle pour GPIO | Lot de 40 câbles |
| **Breadboard** (optionnel) | 1 | Pour prototypage | Breadboard 830 points |

### 3.2 Schéma de Câblage GPIO (1 casier)

```
Raspberry Pi GPIO          Module Relais 1 Canal           Électroaimant
─────────────────          ─────────────────────           ─────────────

GPIO 17 (Pin 11) ────────> IN  ──────> Relais ──────> Électroaimant Casier

GND (Pin 6)      ────────> GND
5V (Pin 2)       ────────> VCC

                           Alimentation 12V
                           ────────────────
                           + 12V ──────> COM (commun du relais)
                           GND   ──────> GND électroaimant
```

### 3.3 Fonctionnement des Électroaimants

**Principe :**
- Électroaimant **alimenté** = porte **verrouillée** (aimant attire la plaque métallique)
- Électroaimant **coupé** = porte **déverrouillée** (aimant relâche la plaque)

**Séquence d'ouverture :**
1. API reçoit la demande d'ouverture du casier X
2. GPIO coupe l'alimentation du relais correspondant (état LOW)
3. Électroaimant se désactive → porte déverrouillée
4. Attendre 5 secondes (temps pour ouvrir la porte)
5. GPIO réactive le relais (état HIGH)
6. Électroaimant se réactive → porte verrouillée

**Code Python exemple :**
```python
import RPi.GPIO as GPIO
import time

# Configuration
GPIO.setmode(GPIO.BCM)
CASIER_PIN = 17  # GPIO 17 pour le casier unique

# Initialisation (verrouillé)
GPIO.setup(CASIER_PIN, GPIO.OUT)
GPIO.output(CASIER_PIN, GPIO.HIGH)  # HIGH = verrouillé

def ouvrir_casier():
    """Déverrouille temporairement le casier"""
    GPIO.output(CASIER_PIN, GPIO.LOW)   # Déverrouiller
    time.sleep(5)                       # Attendre 5 secondes
    GPIO.output(CASIER_PIN, GPIO.HIGH)  # Reverrouiller
    return True

def verrouiller_casier():
    """Verrouille le casier"""
    GPIO.output(CASIER_PIN, GPIO.HIGH)
```

---

## 4. Architecture Technique Retenue

### Stack technologique

| Composant | Technologie |
|-----------|-------------|
| **Serveur / API** | Python + Flask (sur Raspberry Pi) |
| **Base de données** | SQLite (simple) ou MySQL |
| **Interface Client (Kiosk)** | Python + Tkinter **ou** Page Web locale (Chromium kiosk mode) |
| **IHM Commerçant** | Application Web (HTML/CSS/JS) servie par Flask |
| **App Livreur** | Application Web (HTML/CSS/JS) servie par Flask |
| **Email** | Python `smtplib` + compte Gmail SMTP |
| **GPIO / Relais** | Python `RPi.GPIO` |
| **Versioning** | Git + GitHub |

### Structure du projet

```
locker-project/
├── api/                        # Backend Flask (API REST)
│   ├── app.py                  # Point d'entrée Flask
│   ├── config.py               # Configuration (BDD, SMTP, etc.)
│   ├── models.py               # Modèles de données (SQLAlchemy)
│   ├── routes/
│   │   ├── auth.py             # Authentification livreurs
│   │   ├── commandes.py        # Gestion des commandes
│   │   ├── casiers.py          # Gestion des casiers
│   │   ├── livreurs.py         # Gestion des livreurs
│   │   └── locker.py           # Contrôle physique du locker (GPIO)
│   └── utils/
│       ├── email_sender.py     # Envoi de mails
│       └── gpio_controller.py  # Contrôle électroaimants
│
├── web/                        # Frontend Web (servi par Flask)
│   ├── commerçant/             # IHM Commerçant
│   │   ├── index.html
│   │   ├── livreurs.html
│   │   ├── commandes.html
│   │   └── casiers.html
│   ├── livreur/                # Interface Livreur (remplace Android)
│   │   ├── login.html
│   │   ├── commandes.html
│   │   └── livraison.html
│   └── client/                 # Interface Client (Kiosk sur Raspberry)
│       └── index.html          # Saisie code commande + mot de passe
│
├── database/
│   └── schema.sql              # Schéma de la base de données
│
├── docs/
│   └── sysml/                  # Diagrammes SysML
│
└── requirements.txt
```

---

## 4. Modèle de Base de Données

```sql
-- Livreurs
CREATE TABLE livreurs (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    nom         TEXT NOT NULL,
    prenom      TEXT NOT NULL,
    adresse     TEXT,
    login       TEXT UNIQUE NOT NULL,
    password    TEXT NOT NULL,         -- hashé (bcrypt)
    first_login BOOLEAN DEFAULT 1      -- forcer changement mdp
);

-- Commerçants
CREATE TABLE commercants (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    nom     TEXT NOT NULL,
    adresse TEXT NOT NULL
);

-- Casiers
CREATE TABLE casiers (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    taille  TEXT NOT NULL,             -- S, M, L, XL
    etat    TEXT DEFAULT 'libre',      -- libre, occupé, en_attente
    gpio_pin INTEGER                   -- pin GPIO du relais/électroaimant
);

-- Commandes
CREATE TABLE commandes (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    email_client    TEXT NOT NULL,
    taille_casier   TEXT NOT NULL,     -- S, M, L, XL
    poids           REAL,
    commercant_id   INTEGER REFERENCES commercants(id),
    livreur_id      INTEGER REFERENCES livreurs(id),
    casier_id       INTEGER REFERENCES casiers(id),
    code_commande   TEXT UNIQUE,       -- généré automatiquement
    mot_de_passe    TEXT,              -- généré automatiquement
    statut          TEXT DEFAULT 'créée',
    -- statuts: créée → récupérée_par_livreur → déposée → récupérée_par_client
    date_creation   DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_depot      DATETIME,
    date_retrait    DATETIME
);
```

---

## 5. API REST — Endpoints

### Authentification
| Méthode | Route | Description |
|---------|-------|-------------|
| POST | `/api/auth/login` | Connexion livreur (JWT token) |
| POST | `/api/auth/change-password` | Changer le mot de passe (premier login) |

### Commerçant (IHM)
| Méthode | Route | Description |
|---------|-------|-------------|
| GET | `/api/livreurs` | Liste des livreurs |
| POST | `/api/livreurs` | Créer un livreur |
| DELETE | `/api/livreurs/{id}` | Supprimer un livreur |
| GET | `/api/commandes` | Liste des commandes |
| POST | `/api/commandes` | Créer une commande |
| DELETE | `/api/commandes/{id}` | Supprimer une commande |
| GET | `/api/casiers` | État de tous les casiers |
| POST | `/api/commandes/{id}/certifier` | Certifier récupération par livreur |

### Livreur (App Web)
| Méthode | Route | Description |
|---------|-------|-------------|
| GET | `/api/livreur/commandes` | Commandes à récupérer (authentifié) |
| POST | `/api/livreur/commandes/{id}/recuperer` | Valider récupération chez commerçant |
| POST | `/api/livreur/commandes/{id}/deposer` | Déposer dans casier + ouvrir casier |

### Client (Kiosk)
| Méthode | Route | Description |
|---------|-------|-------------|
| POST | `/api/client/retirer` | Entrer code + mot de passe → ouvrir casier |

### Locker physique
| Méthode | Route | Description |
|---------|-------|-------------|
| POST | `/api/casier/{id}/ouvrir` | Ouvrir un casier (GPIO) |
| GET | `/api/casier/{id}/etat` | Lire l'état d'un casier |

---

## 6. Flux Complet d'une Livraison (étape par étape)

```
1. COMMERÇANT crée la commande
   → Saisit : email client, taille casier, poids, son nom/adresse
   → BDD : nouvelle commande (statut = "créée")

2. COMMERÇANT crée le profil du livreur (si pas encore fait)
   → Login + mot de passe temporaire → livreur doit le changer à 1ère connexion

3. LIVREUR se connecte sur l'app web
   → Si premier login : forcé de changer de mot de passe

4. LIVREUR voit les commandes disponibles chez les commerçants
   → Liste avec noms + adresses des commerçants

5. LIVREUR récupère le colis chez le commerçant
   → Clique "Récupéré" → BDD : statut = "récupérée_par_livreur"
   → COMMERÇANT doit certifier depuis son IHM

6. LIVREUR arrive au locker avec le colis
   → Clique "Déposer" → API ouvre automatiquement un casier libre (bonne taille)
   → GPIO déclenche l'électroaimant → casier s'ouvre
   → LIVREUR dépose le colis, referme

7. Raspberry Pi génère automatiquement :
   → Code commande unique (ex: CMD-20240312-0042)
   → Mot de passe aléatoire (ex: 7K3mP9)
   → Envoie un email au CLIENT avec ces deux informations

8. CLIENT va au locker
   → Écran tactile (kiosk) → entre son numéro de commande + mot de passe
   → Si correct : casier s'ouvre automatiquement (GPIO)
   → BDD : statut = "récupérée_par_client", casier redevient "libre"
```

---

## 7. Plan de Réalisation (ordre d'implémentation)

### Phase 1 — Fondations (à faire en premier)
- [ ] **Initialiser le dépôt Git** (GitHub)
- [ ] **Configurer le Raspberry Pi** (IP fixe 192.168.1.116, SSH activé)
- [ ] **Installer l'environnement** : Python 3, Flask, SQLite, pip packages
- [ ] **Créer le schéma de base de données** (`schema.sql`) et l'initialiser
- [ ] **Créer la structure du projet** (dossiers + fichiers vides)

### Phase 2 — Backend (API Flask)
- [ ] **Modèles SQLAlchemy** (Livreur, Commande, Casier, Commerçant)
- [ ] **Route authentification** (login + JWT + changement de mdp premier login)
- [ ] **Routes Commerçant** (CRUD livreurs, CRUD commandes, état casiers)
- [ ] **Routes Livreur** (voir commandes, valider récupération, déposer)
- [ ] **Route Client** (vérifier code + mot de passe → déclencher ouverture)
- [ ] **Envoi d'email** (`smtplib` + Gmail)
- [ ] **Contrôle GPIO** (ouvrir casier via relais/électroaimant)

### Phase 3 — Interfaces Web
- [ ] **IHM Commerçant** (HTML/CSS/JS — gestion livreurs, commandes, casiers)
- [ ] **App Livreur** (HTML/CSS/JS — login, liste commandes, actions)
- [ ] **Interface Client Kiosk** (HTML/CSS plein écran, simple, gros boutons)

### Phase 4 — Maquette Physique
- [ ] **Câblage GPIO → relais → électroaimants** (un relais par casier)
- [ ] **Tests d'ouverture/fermeture** casier par casier
- [ ] **Intégration avec l'API**

### Phase 5 — Intégration & Tests
- [ ] **Tests flux complet** (commande → livraison → retrait client)
- [ ] **Tests des messages d'erreur** (mauvais code, mauvais mdp)
- [ ] **Diagrammes SysML**
- [ ] **Documentation technique**

---

## 8. Installation sur le Raspberry Pi

```bash
# 1. Mise à jour
sudo apt update && sudo apt upgrade -y

# 2. Python et pip
sudo apt install python3 python3-pip python3-venv -y

# 3. Créer l'environnement virtuel
python3 -m venv venv
source venv/bin/activate

# 4. Installer les dépendances
pip install flask flask-sqlalchemy flask-jwt-extended bcrypt RPi.GPIO

# 5. Lancer l'API
python api/app.py
# → Accessible sur http://192.168.1.116:5000
```

---

## 9. Démarrage Automatique au Boot

```bash
# Créer un service systemd
sudo nano /etc/systemd/system/locker-api.service
```

```ini
[Unit]
Description=Locker API Service
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi/locker-project
ExecStart=/home/pi/locker-project/venv/bin/python api/app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable locker-api
sudo systemctl start locker-api
```

---

## 10. Livrables à Rendre (selon le sujet)

| Livrable | Contenu |
|----------|---------|
| **Code source** | Tout le code (API, interfaces web, GPIO) |
| **IHM** | Captures d'écran + démo des interfaces |
| **Maquette** | Locker physique avec Raspberry Pi + électroaimants |
| **Diagrammes SysML** | Diagramme de bloc, de séquence, d'activité |
| **Dossier technique** | Architecture, choix techniques, schéma de câblage |
| **Documentation du code** | Commentaires + README |

---

## 11. Points d'Attention

> ⚠️ **Sécurité** : Ne jamais stocker les mots de passe en clair. Utiliser `bcrypt`.

> ⚠️ **GPIO** : Sur Raspberry Pi 5, le module `RPi.GPIO` peut nécessiter `lgpio`. Vérifier la version.

> ⚠️ **Email** : Utiliser un compte Gmail dédié + mot de passe d'application (pas le vrai mot de passe) pour l'envoi SMTP.

> ⚠️ **Kiosk** : L'interface client sur l'écran tactile du Raspberry doit s'ouvrir automatiquement au démarrage en mode plein écran (Chromium kiosk mode).

> ℹ️ **Réseau** : Le Raspberry Pi doit avoir une **IP fixe** (192.168.1.116 configurée via `dhcpcd.conf` ou depuis la box).

---

*Fichier généré le 05/03/2026 — à mettre à jour au fil du développement*
