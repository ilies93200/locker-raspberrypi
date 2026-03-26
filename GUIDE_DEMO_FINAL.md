# 🎯 GUIDE DÉMO FINAL - Projet Locker 100% Fonctionnel

**Date :** 26 mars 2026  
**IP Raspberry Pi :** 192.168.1.49 (vérifier avec `hostname -I`)  
**Statut :** ✅ OPÉRATIONNEL

---

## ✅ Simplification du Code de Retrait

### NOUVEAU SYSTÈME (SIMPLIFIÉ)
- **Un seul code de 8 caractères** au lieu de code + mot de passe
- Caractères utilisés : **0-9 et A-D** (pavé numérique simple)
- Exemple : `3A7B2C9D`

### Avantages
- ✅ Plus simple pour le client (un seul code à entrer)
- ✅ Compatible avec un pavé numérique 0-9 + A-D
- ✅ 8 caractères = sécurité suffisante (14^8 ≈ 1.4 milliard de combinaisons)

---

## ✅ Corrections Effectuées

### 1. Erreur JWT 422 RÉSOLUE
- **Problème :** `Subject must be a string` - Flask-JWT-Extended attend une string comme identity
- **Solution :** 
  - `create_access_token(identity=str(livreur.id))` dans auth.py
  - `int(get_jwt_identity())` dans toutes les routes protégées

### 2. Code Client Visible Sans Email
- **Problème :** Pas de SMTP configuré pour la démo
- **Solution :** Code commande et mot de passe affichés directement dans les interfaces

---

## 🚀 URLs d'Accès

```
Accueil      : http://192.168.1.49:5000
Commerçant   : http://192.168.1.49:5000/commercant
Livreur      : http://192.168.1.49:5000/livreur
Client       : http://192.168.1.49:5000/client
```

---

## 📋 Workflow Complet de Démonstration

### ÉTAPE 1 : Créer une Commande (Commerçant)

1. Aller sur **http://192.168.1.49:5000/commercant**
2. Section "Gestion des Commandes"
3. Remplir :
   - Email client : `demo@test.com`
   - Taille casier : `M - Moyen`
   - Poids : `2` kg
4. Cliquer **"Créer la commande"**
5. ✅ Commande créée avec statut **"créée"**

---

### ÉTAPE 2 : Certifier la Récupération (Commerçant)

1. Dans la liste des commandes, trouver la commande créée
2. Cliquer sur **"Certifier"**
3. Une popup demande l'ID du livreur
4. Entrer **1** (pour le livreur "ilies khemissi")
5. ✅ Statut passe à **"récupérée_par_livreur"**
6. ✅ La colonne "Livreur" affiche maintenant le nom

---

### ÉTAPE 3 : Connexion Livreur

1. Aller sur **http://192.168.1.49:5000/livreur**
2. Login : `ilies`
3. Mot de passe : `ilies`
4. Cliquer **"Se connecter"**
5. ✅ Redirection automatique vers le dashboard

---

### ÉTAPE 4 : Dashboard Livreur

#### 4.1 Voir les Commandes

**Section "Commandes Disponibles"**
- Commandes avec statut "créée" (à récupérer chez le commerçant)

**Section "Mes Commandes Récupérées"**
- Commandes que tu as récupérées (statut "récupérée_par_livreur")
- Tu devrais voir :

| Email Client | Taille | Poids | Code Retrait | Action |
|--------------|--------|-------|--------------|--------|
| demo@test.com | M | 2kg | - | Déposer dans casier |

#### 4.2 Déposer dans le Casier

1. Cliquer **"Déposer dans le casier"**
2. Confirmer : "Êtes-vous prêt à déposer le colis ?"
3. ✅ **LE CASIER S'OUVRE AUTOMATIQUEMENT** (GPIO 17 - 5 secondes)
4. ✅ **Popup avec les informations client :**

```
✅ Commande déposée avec succès !

🔓 Le casier est ouvert, déposez le colis maintenant.

📋 CODE DE RETRAIT CLIENT :
━━━━━━━━━━━━━━━━━━━━━━━━━━
🔑 3A7B2C9D

💡 Ce code est à communiquer au client pour le retrait.
(8 caractères: chiffres 0-9 et lettres A-D)
```

5. ✅ Le tableau se met à jour :

| Email Client | Taille | Poids | Code Retrait | Action |
|--------------|--------|-------|--------------|--------|
| demo@test.com | M | 2kg | 3A7B2C9D | Voir Code Client |

6. Cliquer **"Voir Code Client"** pour réafficher le code

---

### ÉTAPE 5 : Vérifier Interface Commerçant

1. Aller sur **http://192.168.1.49:5000/commercant**
2. Rafraîchir la page (ou attendre 10 secondes)
3. ✅ Code de retrait visible dans le tableau :

| Email | Taille | Livreur | Statut | Code Retrait | Actions |
|-------|--------|---------|--------|--------------|---------|
| demo@test.com | M | ilies khemissi | déposée | 3A7B2C9D | Infos Retrait |

4. Cliquer **"Infos Retrait"** pour afficher la popup

---

### ÉTAPE 6 : Retrait Client

1. Aller sur **http://192.168.1.49:5000/client**
2. Entrer le code de retrait : `3A7B2C9D`
3. Cliquer **"Ouvrir le casier"**
4. ✅ **LE CASIER S'OUVRE AUTOMATIQUEMENT** (GPIO 17)
5. ✅ Message : "Casier ouvert ! Récupérez votre colis."
6. ✅ Statut passe à **"récupérée_par_client"**
7. ✅ Casier passe à **"libre"**

---

## 🔧 Commandes Utiles

### Vérifier l'IP du Raspberry Pi
```bash
ssh root@192.168.1.49 "hostname -I"
```

### Vérifier le statut du service
```bash
ssh root@192.168.1.49 "systemctl status locker.service"
```

### Voir les logs en temps réel
```bash
ssh root@192.168.1.49 "journalctl -u locker.service -f"
```

### Vérifier la base de données
```bash
ssh root@192.168.1.49 "cd ~/locker-raspberrypi && sqlite3 instance/locker.db 'SELECT id, email_client, statut, code_commande FROM commandes;'"
```

### Redémarrer le service
```bash
ssh root@192.168.1.49 "systemctl restart locker.service"
```

---

## 📦 État Actuel de la BDD

```
Livreur ID=1 : ilies khemissi (login: ilies, mdp: ilies)
Commerçant ID=1 : Boutique Test
Casier ID=1 : Taille M, GPIO 17, État libre
Commande ID=1 : khemissi.ilies93@gmail.com, statut "récupérée_par_livreur"
```

---

## 🎬 Script de Démonstration (5 minutes)

### Minute 1 : Introduction
- Montrer l'interface commerçant
- Expliquer le système de locker

### Minute 2 : Création commande
- Créer une nouvelle commande
- Certifier la récupération par le livreur

### Minute 3 : Livreur
- Se connecter en tant que livreur
- Montrer le dashboard
- Déposer dans le casier
- **MONTRER LE CASIER QUI S'OUVRE** 🔓

### Minute 4 : Informations
- Montrer le code et mot de passe dans l'interface livreur
- Montrer le code et mot de passe dans l'interface commerçant

### Minute 5 : Retrait client
- Interface client kiosk
- Entrer code et mot de passe
- **MONTRER LE CASIER QUI S'OUVRE** 🔓
- Expliquer le workflow complet

---

## ✅ Checklist Avant Démo

- [ ] Raspberry Pi allumé et connecté au réseau
- [ ] Vérifier l'IP avec `hostname -I`
- [ ] Service actif : `systemctl status locker.service`
- [ ] Électroaimant/relais branché sur GPIO 17
- [ ] Alimentation 12V connectée
- [ ] Au moins un livreur créé (login: ilies, mdp: ilies)
- [ ] Navigateur prêt

---

## 🚨 Dépannage

### Erreur 422 JWT
- **Cause :** Token JWT invalide
- **Solution :** Se reconnecter sur /livreur

### Commandes non visibles
- **Cause :** Token expiré ou invalide
- **Solution :** Se déconnecter et se reconnecter

### Casier ne s'ouvre pas
- **Vérifier :** GPIO 17 branché, relais alimenté
- **Test manuel :**
```bash
ssh root@192.168.1.49 "cd ~/locker-raspberrypi && source venv/bin/activate && PYTHONPATH=/root/locker-raspberrypi python3 -c \"
from api.utils.gpio_controller import LockerController
locker = LockerController(17)
locker.ouvrir_casier(3)
\""
```

---

## 📱 Résumé du Workflow

```
COMMERÇANT                    LIVREUR                     CLIENT
    │                            │                           │
    ├─> Crée commande           │                           │
    │   (statut: créée)         │                           │
    │                            │                           │
    ├─> Certifie récupération   │                           │
    │   (statut: récupérée)     │                           │
    │                            │                           │
    │                            ├─> Se connecte             │
    │                            │                           │
    │                            ├─> Voit commande           │
    │                            │   récupérée               │
    │                            │                           │
    │                            ├─> Dépose dans casier      │
    │                            │   🔓 CASIER S'OUVRE       │
    │                            │   📋 CODE + MDP affichés   │
    │                            │   (statut: déposée)       │
    │                            │                           │
    ├─> Voit CODE + MDP         │                           │
    │   dans tableau             │                           │
    │                            │                           │
    │                            │                           ├─> Entre CODE + MDP
    │                            │                           │
    │                            │                           ├─> 🔓 CASIER S'OUVRE
    │                            │                           │   (statut: récupérée_client)
```

---

**🎉 SYSTÈME 100% FONCTIONNEL - PRÊT POUR LA DÉMONSTRATION !**
