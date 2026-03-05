# 🔐 Système de Locker Intelligent

> Projet BTS/Lycée - Casier de livraison connecté avec Raspberry Pi

## 📋 Description

Système de casier intelligent permettant aux commerçants d'un centre-ville piéton de proposer un service de retrait de colis à leurs clients. Le système comprend :

- **Interface Commerçant** : Gestion des livreurs, création de commandes, suivi du casier
- **Interface Livreur** : Authentification, visualisation des commandes, dépôt des colis
- **Interface Client** : Récupération du colis via code de commande et mot de passe
- **Contrôle GPIO** : Ouverture/fermeture automatique du casier via électroaimant
- **Notifications Email** : Envoi automatique des codes au client

## 🛠️ Technologies Utilisées

- **Backend** : Python 3 + Flask
- **Base de données** : SQLite
- **Frontend** : HTML5, CSS3, JavaScript (Vanilla)
- **Hardware** : Raspberry Pi + Module relais + Électroaimant 12V
- **Authentification** : JWT (JSON Web Tokens)
- **Email** : SMTP (Gmail)

## 📁 Structure du Projet

```
locker-project/
├── api/                        # Backend Flask
│   ├── app.py                  # Point d'entrée
│   ├── config.py               # Configuration
│   ├── models.py               # Modèles de données
│   ├── routes/                 # Routes API
│   │   ├── auth.py             # Authentification
│   │   ├── commandes.py        # Gestion commandes
│   │   ├── livreurs.py         # Gestion livreurs
│   │   ├── casiers.py          # Gestion casier
│   │   └── client.py           # Interface client
│   └── utils/
│       ├── email_sender.py     # Envoi emails
│       └── gpio_controller.py  # Contrôle GPIO
├── web/                        # Frontend
│   ├── index.html              # Page d'accueil
│   ├── commercant/             # Interface commerçant
│   ├── livreur/                # Interface livreur
│   ├── client/                 # Interface client (kiosk)
│   └── static/                 # CSS & JS
├── database/
│   └── schema.sql              # Schéma BDD
├── docs/
│   └── sysml/                  # Diagrammes
├── PROJET_LOCKER.md            # Documentation complète
├── requirements.txt            # Dépendances Python
└── README.md                   # Ce fichier
```

## 🚀 Installation sur Raspberry Pi

### 1. Prérequis

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip python3-venv git -y
```

### 2. Cloner le projet

```bash
cd ~
git clone <url-du-repo>
cd locker-project
```

### 3. Créer l'environnement virtuel

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 5. Configurer les variables d'environnement

Créer un fichier `.env` à la racine :

```bash
SECRET_KEY=votre-cle-secrete-ici
JWT_SECRET_KEY=votre-cle-jwt-ici
SMTP_USERNAME=votre-email@gmail.com
SMTP_PASSWORD=votre-mot-de-passe-application-gmail
```

### 6. Initialiser la base de données

```bash
sqlite3 locker.db < database/schema.sql
```

### 7. Lancer le serveur

```bash
python api/app.py
```

Le serveur sera accessible sur :
- **Local** : http://localhost:5000
- **Réseau** : http://192.168.1.116:5000

## 🔌 Câblage GPIO

```
Raspberry Pi GPIO          Module Relais          Électroaimant
─────────────────          ─────────────          ─────────────

GPIO 17 (Pin 11) ────────> IN  ──────> Relais ──────> Électroaimant
GND (Pin 6)      ────────> GND
5V (Pin 2)       ────────> VCC

                           Alimentation 12V
                           ────────────────
                           + 12V ──────> COM (relais)
                           GND   ──────> GND électroaimant
```

## 📱 Utilisation

### Commerçant

1. Accéder à `http://192.168.1.116:5000/commercant`
2. Créer un profil livreur
3. Saisir une nouvelle commande
4. Certifier la récupération par le livreur

### Livreur

1. Accéder à `http://192.168.1.116:5000/livreur`
2. Se connecter avec login/mot de passe
3. Voir les commandes disponibles
4. Déposer le colis dans le casier

### Client

1. Recevoir l'email avec code de commande + mot de passe
2. Se rendre au locker (écran tactile)
3. Accéder à `http://localhost:5000/client`
4. Entrer le code et mot de passe
5. Le casier s'ouvre automatiquement

## 🔧 API REST

### Authentification

- `POST /api/auth/login` - Connexion livreur
- `POST /api/auth/change-password` - Changer mot de passe
- `GET /api/auth/me` - Infos utilisateur connecté

### Livreurs

- `GET /api/livreurs` - Liste des livreurs
- `POST /api/livreurs` - Créer un livreur
- `DELETE /api/livreurs/{id}` - Supprimer un livreur

### Commandes

- `GET /api/commandes` - Liste des commandes
- `POST /api/commandes` - Créer une commande
- `POST /api/commandes/{id}/certifier` - Certifier récupération
- `POST /api/commandes/{id}/deposer` - Déposer dans casier
- `DELETE /api/commandes/{id}` - Supprimer commande

### Casier

- `GET /api/casiers` - État du casier
- `POST /api/casiers/1/ouvrir` - Ouvrir casier (test)

### Client

- `POST /api/client/retirer` - Retirer commande

## 🎓 Livrables pour le Professeur

- ✅ Code source complet
- ✅ Documentation technique (PROJET_LOCKER.md)
- ✅ Schéma de base de données
- ✅ Diagrammes SysML (à compléter dans `docs/sysml/`)
- ✅ Guide d'installation (ce README)
- ✅ Maquette physique (Raspberry Pi + électroaimant)

## 🐛 Dépannage

### Le GPIO ne fonctionne pas

Sur Raspberry Pi 5, installer `lgpio` :
```bash
pip install rpi-lgpio
```

### Erreur d'envoi d'email

1. Activer la validation en 2 étapes sur Gmail
2. Générer un "mot de passe d'application"
3. Utiliser ce mot de passe dans `.env`

### Le serveur n'est pas accessible depuis le réseau

Vérifier l'IP du Raspberry Pi :
```bash
hostname -I
```

Configurer une IP fixe dans `/etc/dhcpcd.conf` :
```
interface wlan0
static ip_address=192.168.1.116/24
static routers=192.168.1.1
static domain_name_servers=192.168.1.1
```

## 👨‍🎓 Auteur

Projet réalisé dans le cadre d'un projet BTS/Lycée

## 📄 Licence

Ce projet est à usage éducatif uniquement.
