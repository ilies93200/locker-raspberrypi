# 🎯 Guide Workflow Complet - Démonstration Projet Locker

**Date :** 18 mars 2026  
**Système :** 100% Opérationnel sur Raspberry Pi (192.168.1.116)

---

## 📋 État Actuel de la Base de Données

```sql
Commerçant : Boutique Test (ID=1)
Casier : Taille M, GPIO 17, État libre
Livreur : ilies khemissi (login: ilies)
Commande : 1 commande en statut "récupérée_par_livreur"
```

---

## 🚀 Workflow Complet de Démonstration

### ÉTAPE 1 : Interface Commerçant
**URL :** http://192.168.1.116:5000/commercant

#### 1.1 Créer un Nouveau Livreur (si besoin)
1. Section "Gestion des Livreurs"
2. Remplir :
   - Nom : `Dupont`
   - Prénom : `Jean`
   - Adresse : `10 Rue de Paris`
   - Login : `jdupont`
   - Mot de passe : `test123`
3. Cliquer "Créer le livreur"
4. ✅ Le livreur apparaît dans la liste

#### 1.2 Créer une Nouvelle Commande
1. Section "Gestion des Commandes"
2. Remplir :
   - Email client : `client@example.com`
   - Taille du casier : `M - Moyen`
   - Poids : `2.5` kg
3. Cliquer "Créer la commande"
4. ✅ Commande créée avec statut **"créée"**

#### 1.3 Certifier la Récupération par le Livreur
1. Dans "Liste des commandes", trouver la commande créée
2. Cliquer sur le bouton **"Certifier"**
3. Une popup affiche : `ID du livreur (1: ilies khemissi, 2: Jean Dupont):`
4. Entrer l'ID du livreur (ex: `1` pour ilies)
5. ✅ Statut passe à **"récupérée_par_livreur"**
6. ✅ La colonne "Livreur" affiche maintenant le nom du livreur

**Ce que tu vois maintenant :**
```
Email Client         | Taille | Livreur          | Statut                  | Code | Mot de Passe | Actions
---------------------|--------|------------------|-------------------------|------|--------------|----------
client@example.com   | M      | ilies khemissi   | récupérée_par_livreur   | -    | -            | Supprimer
```

---

### ÉTAPE 2 : Connexion Livreur
**URL :** http://192.168.1.116:5000/livreur

1. Entrer les identifiants :
   - Login : `ilies`
   - Mot de passe : (celui que tu as créé)
2. Cliquer "Se connecter"
3. ✅ Redirection automatique vers le dashboard

---

### ÉTAPE 3 : Dashboard Livreur
**URL :** http://192.168.1.116:5000/livreur/dashboard

#### 3.1 Vue des Commandes

**Section "Commandes Disponibles"**
- Affiche les commandes avec statut "créée" (à récupérer chez le commerçant)
- Actuellement : Aucune (car la commande est déjà "récupérée_par_livreur")

**Section "Mes Commandes Récupérées"**
- Affiche les commandes que tu as récupérées
- Tu devrais voir :

```
Email Client         | Taille | Poids | Code Commande | Mot de Passe | Action
---------------------|--------|-------|---------------|--------------|------------------
client@example.com   | M      | 2.5kg | -             | -            | Déposer dans casier
```

#### 3.2 Déposer la Commande dans le Casier

1. Cliquer sur **"Déposer dans le casier"**
2. Confirmer : "Êtes-vous prêt à déposer le colis ?"
3. ✅ **Le casier s'ouvre automatiquement pendant 5 secondes** (GPIO)
4. ✅ Une popup s'affiche avec :

```
✅ Commande déposée avec succès !

🔓 Le casier est ouvert, déposez le colis maintenant.

📋 INFORMATIONS CLIENT :
━━━━━━━━━━━━━━━━━━━━━━━━━━
🔑 Code Commande: CMD-20260318-1234
🔐 Mot de Passe: A7K9P2

💡 Ces informations sont à communiquer au client pour le retrait.
```

5. ✅ Le tableau se met à jour :

```
Email Client         | Taille | Poids | Code Commande      | Mot de Passe | Action
---------------------|--------|-------|--------------------|--------------|-----------------
client@example.com   | M      | 2.5kg | CMD-20260318-1234  | A7K9P2       | Voir Infos Client
```

6. Tu peux cliquer sur **"Voir Infos Client"** pour réafficher les informations

---

### ÉTAPE 4 : Retour Interface Commerçant
**URL :** http://192.168.1.116:5000/commercant

Rafraîchir la page (ou attendre 10 secondes, auto-refresh)

**Ce que tu vois maintenant :**
```
Email Client         | Taille | Livreur          | Statut   | Code Commande      | Mot de Passe | Actions
---------------------|--------|------------------|----------|--------------------|--------------|--------------
client@example.com   | M      | ilies khemissi   | déposée  | CMD-20260318-1234  | A7K9P2       | Infos Retrait
                     |        |                  |          |                    |              | Supprimer
```

✅ Le commerçant peut voir le **code** et **mot de passe** pour les communiquer au client

Cliquer sur **"Infos Retrait"** affiche une popup avec toutes les informations :
```
📦 INFORMATIONS DE RETRAIT
━━━━━━━━━━━━━━━━━━━━━━━━━━

👤 Client: client@example.com
🔑 Code Commande: CMD-20260318-1234
🔐 Mot de Passe: A7K9P2

📱 À communiquer au client pour le retrait
```

---

### ÉTAPE 5 : Retrait Client
**URL :** http://192.168.1.116:5000/client

#### 5.1 Interface Kiosk Client

1. Le client entre :
   - **Code de commande :** `CMD-20260318-1234`
   - **Mot de passe :** `A7K9P2`
2. Cliquer "Ouvrir le casier"
3. ✅ **Le casier s'ouvre automatiquement** (GPIO)
4. ✅ Message de succès : "Casier ouvert ! Récupérez votre colis."
5. ✅ Statut de la commande passe à **"récupérée_par_client"**
6. ✅ État du casier passe à **"libre"**

---

## 📊 Résumé du Workflow

```
1. COMMERÇANT
   └─> Crée commande (statut: "créée")
   └─> Certifie récupération par livreur (statut: "récupérée_par_livreur")

2. LIVREUR
   └─> Se connecte au dashboard
   └─> Voit la commande dans "Mes Commandes Récupérées"
   └─> Clique "Déposer dans le casier"
   └─> 🔓 CASIER S'OUVRE (GPIO)
   └─> Reçoit CODE + MOT DE PASSE dans popup
   └─> Peut voir les infos à tout moment (statut: "déposée")

3. COMMERÇANT (optionnel)
   └─> Voit CODE + MOT DE PASSE dans la liste
   └─> Peut cliquer "Infos Retrait" pour les afficher
   └─> Communique au client par téléphone/SMS

4. CLIENT
   └─> Va sur l'interface kiosk
   └─> Entre CODE + MOT DE PASSE
   └─> 🔓 CASIER S'OUVRE (GPIO)
   └─> Récupère le colis (statut: "récupérée_par_client")
```

---

## 🎯 Points Clés pour la Démo

### ✅ Fonctionnalités Visibles

1. **Gestion Multi-Utilisateurs**
   - Interface commerçant (admin)
   - Interface livreur (authentification JWT)
   - Interface client (kiosk public)

2. **Contrôle Physique**
   - Ouverture automatique du casier via GPIO
   - Électroaimant contrôlé par Raspberry Pi
   - Durée d'ouverture : 5 secondes

3. **Sécurité**
   - Code commande unique (ex: CMD-20260318-1234)
   - Mot de passe aléatoire 6 caractères (ex: A7K9P2)
   - Authentification JWT pour livreurs

4. **Traçabilité**
   - Statuts de commande : créée → récupérée_par_livreur → déposée → récupérée_par_client
   - Dates enregistrées pour chaque étape
   - Historique complet dans la BDD

5. **Affichage des Informations (SANS EMAIL)**
   - ✅ Code et mot de passe visibles dans interface commerçant
   - ✅ Code et mot de passe visibles dans interface livreur
   - ✅ Popup avec infos complètes après dépôt
   - ✅ Bouton "Voir Infos Client" dans dashboard livreur

---

## 🔍 Vérifications Techniques

### Vérifier l'État du Système

```bash
# Statut du service
ssh root@192.168.1.116 "systemctl status locker.service"

# Logs en temps réel
ssh root@192.168.1.116 "journalctl -u locker.service -f"

# État de la BDD
ssh root@192.168.1.116 "cd ~/locker-raspberrypi && sqlite3 instance/locker.db 'SELECT id, email_client, statut, code_commande FROM commandes;'"
```

### Tester le GPIO Manuellement

```bash
ssh root@192.168.1.116 "cd ~/locker-raspberrypi && python3 << 'EOF'
import sys
sys.path.insert(0, '/root/locker-raspberrypi')
from api.utils.gpio_controller import LockerController
controller = LockerController(17)
controller.ouvrir_casier(duree=3)
EOF
"
```

---

## 🎬 Script de Démonstration

### Scénario Complet (5 minutes)

**Minute 1-2 : Création de la commande**
- Montrer l'interface commerçant
- Créer une commande pour un client
- Certifier la récupération par le livreur

**Minute 2-3 : Livreur**
- Se connecter en tant que livreur
- Montrer la commande dans "Mes Commandes Récupérées"
- Déposer dans le casier
- **MONTRER LE CASIER QUI S'OUVRE** 🔓
- Montrer la popup avec code/mot de passe

**Minute 3-4 : Informations visibles**
- Retourner sur interface commerçant
- Montrer que le code et mot de passe sont visibles
- Cliquer "Infos Retrait" pour afficher la popup

**Minute 4-5 : Retrait client**
- Aller sur interface client (kiosk)
- Entrer le code et mot de passe
- **MONTRER LE CASIER QUI S'OUVRE** 🔓
- Expliquer que le statut passe à "récupérée_par_client"

---

## 📱 Informations Importantes

### Pas Besoin d'Email pour la Démo

✅ Toutes les informations (code commande + mot de passe) sont visibles dans :
- Interface commerçant (tableau + popup "Infos Retrait")
- Interface livreur (tableau + popup après dépôt + bouton "Voir Infos Client")

Le commerçant peut communiquer ces infos au client par :
- Téléphone
- SMS
- En personne
- Affichage sur écran

### URLs à Retenir

- **Accueil :** http://192.168.1.116:5000
- **Commerçant :** http://192.168.1.116:5000/commercant
- **Livreur :** http://192.168.1.116:5000/livreur
- **Client :** http://192.168.1.116:5000/client

### Identifiants

- **Livreur actuel :** login `ilies` / mot de passe (celui que tu as créé)
- **Commerçant :** Pas de login (accès direct)

---

## ✅ Checklist Avant la Démo

- [ ] Raspberry Pi allumé et connecté au réseau
- [ ] Service locker.service actif (`systemctl status locker.service`)
- [ ] Électroaimant et relais branchés sur GPIO 17
- [ ] Alimentation 12V connectée
- [ ] Base de données initialisée avec commerçant et casier
- [ ] Au moins un livreur créé
- [ ] Navigateur web prêt (Chrome/Firefox)
- [ ] Connexion au réseau local 192.168.1.x

---

**Projet prêt pour la démonstration ! 🚀**
