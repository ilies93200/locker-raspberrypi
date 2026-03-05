# 🚀 Guide pour Push sur GitHub

## Dépôt GitHub
**URL :** https://github.com/ilies93200/locker-raspberrypi.git

---

## 📝 Commandes à Exécuter

### 1. Initialiser Git (si pas déjà fait)

```bash
cd "c:\Users\khemi\OneDrive\Desktop\Projet Raspberrypi"
git init
```

### 2. Ajouter le dépôt distant

```bash
git remote add origin https://github.com/ilies93200/locker-raspberrypi.git
```

Si le remote existe déjà, le mettre à jour :
```bash
git remote set-url origin https://github.com/ilies93200/locker-raspberrypi.git
```

### 3. Ajouter tous les fichiers

```bash
git add .
```

### 4. Créer le commit

```bash
git commit -m "Initial commit - Projet Locker Intelligent complet"
```

### 5. Pousser sur GitHub

```bash
git branch -M main
git push -u origin main
```

Si le dépôt existe déjà et tu veux forcer :
```bash
git push -u origin main --force
```

---

## 🔑 Authentification GitHub

Si GitHub demande une authentification :

### Option 1 : Personal Access Token (Recommandé)

1. Va sur GitHub : https://github.com/settings/tokens
2. Clique sur "Generate new token" → "Generate new token (classic)"
3. Donne un nom : "Locker Raspberry Pi"
4. Coche : `repo` (accès complet aux dépôts)
5. Génère le token
6. **Copie le token** (tu ne pourras plus le voir après)

Quand Git demande le mot de passe, colle le **token** (pas ton mot de passe GitHub).

### Option 2 : GitHub CLI (Plus simple)

```bash
# Installer GitHub CLI
winget install --id GitHub.cli

# Se connecter
gh auth login

# Puis faire le push normalement
git push -u origin main
```

---

## 📋 Commandes Complètes (Copier-Coller)

```bash
# Aller dans le dossier du projet
cd "c:\Users\khemi\OneDrive\Desktop\Projet Raspberrypi"

# Initialiser Git
git init

# Configurer ton identité (remplace par tes infos)
git config user.name "ilies93200"
git config user.email "ton-email@example.com"

# Ajouter le dépôt distant
git remote add origin https://github.com/ilies93200/locker-raspberrypi.git

# Ajouter tous les fichiers
git add .

# Créer le commit
git commit -m "Initial commit - Projet Locker Intelligent complet

- API Flask REST complète
- Interfaces web (commerçant, livreur, client)
- Contrôle GPIO pour électroaimant
- Base de données SQLite
- Envoi d'emails automatique
- Documentation complète
- Guide d'installation
"

# Pousser sur GitHub
git branch -M main
git push -u origin main
```

---

## ✅ Vérification

Après le push, va sur :
https://github.com/ilies93200/locker-raspberrypi

Tu devrais voir tous tes fichiers !

---

## 🔧 En Cas de Problème

### Erreur : "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/ilies93200/locker-raspberrypi.git
```

### Erreur : "failed to push some refs"
```bash
git pull origin main --allow-unrelated-histories
git push -u origin main
```

### Erreur : "Authentication failed"
- Utilise un Personal Access Token au lieu de ton mot de passe
- Ou installe GitHub CLI : `gh auth login`

---

## 📦 Fichiers qui Seront Poussés

```
✅ PROJET_LOCKER.md (documentation complète)
✅ README.md (guide d'utilisation)
✅ GUIDE_INSTALLATION_PROF.md (guide pour le prof)
✅ RENDU_PROJET.md (dossier de rendu)
✅ requirements.txt
✅ install.sh
✅ .gitignore
✅ api/ (tout le backend Flask)
✅ web/ (toutes les interfaces web)
✅ database/ (schéma SQL)
✅ docs/ (pour les diagrammes SysML)
```

**Total :** ~30 fichiers, ~2000 lignes de code

---

## 🎯 Après le Push

Ton prof pourra cloner le projet avec :

```bash
git clone https://github.com/ilies93200/locker-raspberrypi.git
cd locker-raspberrypi
chmod +x install.sh
./install.sh
```

Et tout sera prêt à fonctionner ! 🚀
