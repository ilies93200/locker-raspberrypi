# 🍓 Installation sur Raspberry Pi

## 📋 Commandes à Exécuter (Copier-Coller)

### 1. Se Connecter au Raspberry Pi

Depuis ton PC Windows, ouvre PowerShell et connecte-toi :

```powershell
ssh root@192.168.1.116
# Mot de passe : ilies
```

---

### 2. Une Fois Connecté au Raspberry Pi

Copie-colle ces commandes **une par une** :

```bash
# Aller dans le dossier home
cd ~

# Mettre à jour le système
sudo apt update && sudo apt upgrade -y

# Installer Git
sudo apt install git -y

# Cloner le projet depuis GitHub
git clone https://github.com/ilies93200/locker-raspberrypi.git

# Aller dans le dossier du projet
cd locker-raspberrypi

# Installer Python et dépendances système
sudo apt install python3 python3-pip python3-venv -y

# Créer l'environnement virtuel Python
python3 -m venv venv

# Activer l'environnement virtuel
source venv/bin/activate

# Mettre à jour pip
pip install --upgrade pip

# Installer les dépendances Python
pip install -r requirements.txt

# Initialiser la base de données
python3 << 'EOF'
from api.app import app, db
with app.app_context():
    db.create_all()
    print("✅ Base de données initialisée")
EOF

# Configurer l'IP fixe (optionnel mais recommandé)
echo "
interface eth0
static ip_address=192.168.1.116/24
static routers=192.168.1.1
static domain_name_servers=192.168.1.1
" | sudo tee -a /etc/dhcpcd.conf

# Redémarrer le service réseau
sudo systemctl restart dhcpcd

# Donner les permissions GPIO
sudo usermod -a -G gpio root

echo ""
echo "✅ Installation terminée !"
echo ""
echo "Pour démarrer le serveur :"
echo "  cd ~/locker-raspberrypi"
echo "  source venv/bin/activate"
echo "  python api/app.py"
```

---

### 3. Démarrer le Serveur

```bash
cd ~/locker-raspberrypi
source venv/bin/activate
python api/app.py
```

Le serveur sera accessible sur :
- **Local** : http://localhost:5000
- **Réseau** : http://192.168.1.116:5000

---

### 4. Démarrage Automatique au Boot (Optionnel)

Pour que le serveur démarre automatiquement au démarrage du Raspberry Pi :

```bash
# Créer le service systemd
sudo nano /etc/systemd/system/locker.service
```

Copie ce contenu dans le fichier :

```ini
[Unit]
Description=Locker API Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/locker-raspberrypi
ExecStart=/root/locker-raspberrypi/venv/bin/python /root/locker-raspberrypi/api/app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Sauvegarde (Ctrl+X, Y, Enter), puis :

```bash
# Recharger systemd
sudo systemctl daemon-reload

# Activer le service au démarrage
sudo systemctl enable locker.service

# Démarrer le service
sudo systemctl start locker.service

# Vérifier le statut
sudo systemctl status locker.service
```

---

### 5. Vérifier que Tout Fonctionne

```bash
# Tester l'API
curl http://localhost:5000/api/casiers

# Devrait retourner :
# {"id":1,"taille":"M","etat":"libre","gpio_pin":17}
```

---

### 6. Accéder aux Interfaces Web

Depuis n'importe quel appareil sur le réseau local, ouvre un navigateur :

- **Page d'accueil** : http://192.168.1.116:5000
- **Interface Commerçant** : http://192.168.1.116:5000/commercant
- **Interface Livreur** : http://192.168.1.116:5000/livreur
- **Interface Client** : http://192.168.1.116:5000/client

---

## 🔧 Commandes Utiles

### Voir les logs du serveur
```bash
sudo journalctl -u locker.service -f
```

### Arrêter le serveur
```bash
sudo systemctl stop locker.service
```

### Redémarrer le serveur
```bash
sudo systemctl restart locker.service
```

### Mettre à jour le projet depuis GitHub
```bash
cd ~/locker-raspberrypi
git pull origin main
sudo systemctl restart locker.service
```

---

## 🐛 Dépannage

### Le serveur ne démarre pas

```bash
# Vérifier les logs
sudo journalctl -u locker.service -n 50

# Tester manuellement
cd ~/locker-raspberrypi
source venv/bin/activate
python api/app.py
```

### GPIO ne fonctionne pas

```bash
# Vérifier les permissions
sudo usermod -a -G gpio root
sudo reboot
```

### Port 5000 déjà utilisé

```bash
# Trouver le processus
sudo lsof -i :5000

# Tuer le processus
sudo kill -9 <PID>
```

---

## ✅ Checklist d'Installation

- [ ] Connexion SSH au Raspberry Pi réussie
- [ ] Git installé
- [ ] Projet cloné depuis GitHub
- [ ] Environnement virtuel Python créé
- [ ] Dépendances installées
- [ ] Base de données initialisée
- [ ] Serveur démarre sans erreur
- [ ] Interfaces web accessibles depuis le réseau
- [ ] GPIO fonctionne (test d'ouverture du casier)
- [ ] Service systemd configuré (optionnel)

---

## 🎯 Test Complet

Une fois tout installé, teste le flux complet :

1. Va sur http://192.168.1.116:5000/commercant
2. Crée un livreur
3. Crée une commande
4. Va sur http://192.168.1.116:5000/livreur
5. Connecte-toi
6. Récupère la commande
7. Dépose dans le casier → **Le casier s'ouvre !**
8. Va sur http://192.168.1.116:5000/client
9. Entre le code reçu par email
10. **Le casier s'ouvre à nouveau !**

---

**Temps d'installation estimé :** 10-15 minutes

Bon courage ! 🚀
