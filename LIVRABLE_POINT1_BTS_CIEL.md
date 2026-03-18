# BTS CIEL - Projet de Fin de Cursus
## Trame de Préparation - Point n°1

**Date du point :** 19 février 2025  
**Phase :** Démarrage (19/02/25 → 19/03/25)  
**Livrable attendu pour le 19 février 2025**

---

## 1. Présentation du Projet

### Intitulé du Projet
**Système de Casier Intelligent Connecté pour Commerce de Proximité**

### Contexte
Les commerçants d'un centre-ville piéton souhaitent offrir un service de retrait de commandes en dehors des horaires d'ouverture. Les clients commandent en ligne ou en boutique, et peuvent récupérer leurs achats 24h/24 via un casier intelligent sécurisé.

**Problématique :** Comment permettre aux clients de récupérer leurs commandes de manière autonome et sécurisée ?

**Besoin résolu :**
- Flexibilité horaire pour les clients (retrait 24h/24)
- Réduction de la charge de travail pour les commerçants
- Optimisation de la logistique de livraison
- Traçabilité complète des opérations

### Objectifs Principaux

1. **Contrôle physique du casier** : Système d'ouverture/fermeture automatique via électroaimant 12V contrôlé par Raspberry Pi
2. **Gestion multi-utilisateurs** : Interfaces web distinctes pour commerçants, livreurs et clients
3. **Sécurité et traçabilité** : Authentification JWT, codes uniques par commande, logs complets

### Périmètre du Projet

**Inclus :**
- Backend API REST (Flask/Python)
- Base de données SQLite locale
- Contrôle GPIO pour 1 casier (extensible à 4)
- 3 interfaces web (commerçant, livreur, client)
- Système de notifications email
- Authentification sécurisée (JWT + bcrypt)
- Documentation technique complète

**Exclus :**
- Application mobile native (remplacée par web app)
- Hébergement cloud (système 100% local)
- Système de paiement en ligne
- Reconnaissance faciale

---

## 2. Équipe et Organisation

### Composition de l'Équipe

| Membre | Rôle Principal | Responsabilités |
|--------|----------------|-----------------|
| **Étudiant 1** | Développeur Backend + Hardware | - API Flask REST<br>- Contrôle GPIO Raspberry Pi<br>- Gestion base de données<br>- Intégration électroaimant |
| **Étudiant 2** | Développeur Frontend | - Interface commerçant<br>- Interface livreur<br>- Interface client (kiosk)<br>- Design UI/UX |
| **Étudiant 3** | Intégrateur Système | - Configuration Raspberry Pi<br>- Tests d'intégration<br>- Documentation<br>- Câblage électronique |

### Répartition des Tâches

**Backend (Étudiant 1) :**
- Modèles de données (Livreur, Commande, Casier, Commerçant)
- Routes API REST (auth, commandes, casiers, client)
- Contrôleur GPIO (ouverture/fermeture casier)
- Système d'envoi d'emails (SMTP)

**Frontend (Étudiant 2) :**
- Interface commerçant (gestion livreurs + commandes)
- Interface livreur (authentification + dépôt)
- Interface client kiosk (retrait avec code)
- Styles CSS et responsive design

**Intégration (Étudiant 3) :**
- Installation et configuration Raspberry Pi
- Câblage GPIO + relais + électroaimant
- Tests fonctionnels bout-en-bout
- Rédaction guides d'installation et utilisation

### Outils de Collaboration
- **Git/GitHub** : Versioning du code (https://github.com/ilies93200/locker-raspberrypi)
- **Discord** : Communication quotidienne
- **Trello** : Suivi des tâches et planning
- **Google Drive** : Documentation partagée

---

## 3. Analyse Technique Préliminaire

### Technologies Envisagées

#### Backend
- **Langage :** Python 3.11+
  - *Justification :* Excellent support GPIO sur Raspberry Pi, bibliothèques riches (Flask, SQLAlchemy), syntaxe claire
- **Framework :** Flask 3.0
  - *Justification :* Léger, flexible, parfait pour API REST, documentation complète
- **Base de données :** SQLite
  - *Justification :* Embarquée, sans serveur, suffisante pour usage local, facile à sauvegarder

#### Frontend
- **Technologies :** HTML5, CSS3, JavaScript Vanilla
  - *Justification :* Pas de dépendances lourdes, compatible tous navigateurs, performance optimale
- **Frameworks CSS :** TailwindCSS (optionnel)
  - *Justification :* Design moderne rapide, responsive natif

#### Hardware
- **Plateforme :** Raspberry Pi 4 Model B
  - *Justification :* GPIO intégré, puissance suffisante pour serveur web, Linux natif
- **Contrôle :** RPi.GPIO / lgpio
  - *Justification :* Bibliothèque standard pour contrôle GPIO
- **Électronique :** Module relais 5V + Électroaimant 12V
  - *Justification :* Isolation électrique, sécurité, fiabilité

#### Sécurité
- **Authentification :** JWT (JSON Web Tokens)
  - *Justification :* Stateless, sécurisé, standard industrie
- **Hachage :** bcrypt
  - *Justification :* Algorithme robuste contre brute-force
- **HTTPS :** Certificat auto-signé (optionnel)
  - *Justification :* Chiffrement des communications

### Architecture Pressentie

```
┌─────────────────────────────────────────────────────────────┐
│                    RASPBERRY PI 4                           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              SERVEUR WEB FLASK                       │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐     │   │
│  │  │   Routes   │  │   Models   │  │   Utils    │     │   │
│  │  │    API     │  │ SQLAlchemy │  │ GPIO/Email │     │   │
│  │  └────────────┘  └────────────┘  └────────────┘     │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │           BASE DE DONNÉES SQLite                     │   │
│  │  [Livreurs] [Commandes] [Casiers] [Commerçants]     │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              CONTRÔLE GPIO                           │   │
│  │  GPIO 17 → Relais 5V → Électroaimant 12V            │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                          ↓ HTTP (port 5000)
┌─────────────────────────────────────────────────────────────┐
│                  INTERFACES WEB (Navigateur)                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Commerçant  │  │   Livreur    │  │    Client    │      │
│  │   (Admin)    │  │ (Auth JWT)   │  │   (Kiosk)    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

**Schéma simplifié Client/Serveur :**
- **Serveur :** Raspberry Pi (192.168.1.116:5000)
- **Clients :** Navigateurs web sur réseau local
- **Communication :** HTTP/JSON (API REST)
- **Stockage :** SQLite local (instance/locker.db)

### Contraintes Identifiées

**Matérielles :**
- Alimentation stable 12V/2A pour électroaimant
- Dissipation thermique du relais
- Câblage sécurisé (isolation électrique)

**Logicielles :**
- Compatibilité RPi.GPIO avec Raspberry Pi 5 (migration vers lgpio si nécessaire)
- Gestion concurrence (plusieurs utilisateurs simultanés)
- Timeout réseau (connexion SMTP Gmail)

**Temps :**
- Délai serré (1 mois jusqu'à Revue 1)
- Tests matériels nécessitant le Raspberry Pi physique
- Apprentissage Flask/SQLAlchemy pour certains membres

---

## 4. Planification

### Découpage en Grandes Phases

| Phase | Période | Objectifs | Livrables |
|-------|---------|-----------|-----------|
| **Phase 1 : Démarrage** | 19/02 - 26/02 | Setup environnement, architecture | Repo Git, schéma BDD, maquettes |
| **Phase 2 : Développement** | 27/02 - 12/03 | Code backend + frontend | API fonctionnelle, interfaces web |
| **Phase 3 : Intégration** | 13/03 - 19/03 | Tests hardware, déploiement | Système complet opérationnel |
| **Phase 4 : Finalisation** | 20/03 - 19/04 | Documentation, optimisations | Livrable final pour Revue 1 |

### Livrables Attendus pour la Revue 1 (19/03/25)

1. ✅ **Code source complet** (GitHub)
2. ✅ **Base de données fonctionnelle** (SQLite avec données de test)
3. ✅ **API REST opérationnelle** (15 endpoints documentés)
4. ✅ **3 interfaces web** (commerçant, livreur, client)
5. ✅ **Contrôle GPIO fonctionnel** (ouverture/fermeture casier)
6. ✅ **Documentation technique** (README, guide installation, guide prof)
7. ✅ **Maquette physique** (Raspberry Pi + relais + électroaimant)
8. ⏳ **Présentation PowerPoint** (10-15 slides)
9. ⏳ **Vidéo démo** (3-5 minutes)

### Risques Identifiés

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| **Incompatibilité GPIO Raspberry Pi 5** | Moyenne | Élevé | Prévoir migration vers lgpio, tester tôt |
| **Délai livraison matériel** | Faible | Élevé | Commander immédiatement, mode simulation en attendant |
| **Blocage SMTP Gmail** | Élevée | Moyen | Utiliser mot de passe d'application, prévoir alternative (Mailgun) |
| **Surcharge planning** | Moyenne | Moyen | Prioriser fonctionnalités core, reporter features secondaires |
| **Bugs concurrence BDD** | Moyenne | Moyen | Tests unitaires, gestion transactions SQLAlchemy |
| **Manque compétences Flask** | Faible | Faible | Tutoriels en ligne, pair programming |

### Planning Prévisionnel avec Jalons

**Semaine 1 (19/02 - 26/02) :**
- ✅ Création repo GitHub
- ✅ Schéma base de données (schema.sql)
- ✅ Modèles SQLAlchemy (models.py)
- ✅ Structure projet complète
- 🎯 **Jalon 1 :** Architecture validée

**Semaine 2 (27/02 - 05/03) :**
- ✅ Routes API REST (auth, commandes, casiers)
- ✅ Contrôleur GPIO (gpio_controller.py)
- ✅ Interface commerçant (HTML/CSS/JS)
- 🎯 **Jalon 2 :** Backend fonctionnel

**Semaine 3 (06/03 - 12/03) :**
- ✅ Interface livreur (login + dashboard)
- ✅ Interface client kiosk
- ✅ Système d'envoi emails
- 🎯 **Jalon 3 :** Frontend complet

**Semaine 4 (13/03 - 19/03) :**
- ✅ Installation Raspberry Pi
- ✅ Câblage électronique
- ✅ Tests d'intégration bout-en-bout
- ✅ Documentation finale
- 🎯 **REVUE 1 (19/03/25)**

---

## 5. Conclusion

Ce projet de casier intelligent connecté répond à un besoin réel des commerçants de proximité tout en permettant de mettre en pratique les compétences acquises en BTS CIEL :

- **Développement logiciel** : API REST, bases de données, interfaces web
- **Systèmes embarqués** : Raspberry Pi, contrôle GPIO, électronique
- **Gestion de projet** : Planning, travail d'équipe, documentation

L'architecture technique choisie (Flask + SQLite + Raspberry Pi) est adaptée au contexte local et permet une réalisation dans les délais impartis.

**État actuel (05/03/26) :** Le projet est **opérationnel** avec toutes les fonctionnalités core implémentées. Le système est déployé sur le Raspberry Pi (192.168.1.116) et accessible sur le réseau local.

---

**Signatures :**

| Rôle | Nom | Date | Signature |
|------|-----|------|-----------|
| Chef de projet | [Nom] | 19/02/2025 | |
| Développeur Backend | [Nom] | 19/02/2025 | |
| Développeur Frontend | [Nom] | 19/02/2025 | |

---

*Document généré le 18/03/2026*  
*Version 1.0 - Livrable Point n°1*
