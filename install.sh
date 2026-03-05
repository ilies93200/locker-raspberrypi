#!/bin/bash

echo "🚀 Installation du système de Locker Intelligent"
echo "=================================================="
echo ""

echo "📦 Mise à jour du système..."
sudo apt update && sudo apt upgrade -y

echo ""
echo "🐍 Installation de Python et dépendances..."
sudo apt install python3 python3-pip python3-venv -y

echo ""
echo "📁 Création de l'environnement virtuel..."
python3 -m venv venv

echo ""
echo "⚙️  Activation de l'environnement virtuel..."
source venv/bin/activate

echo ""
echo "📚 Installation des packages Python..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "🗄️  Initialisation de la base de données..."
python3 << EOF
from api.app import app, db
with app.app_context():
    db.create_all()
    print("✅ Base de données initialisée")
EOF

echo ""
echo "✅ Installation terminée !"
echo ""
echo "Pour démarrer le serveur :"
echo "  source venv/bin/activate"
echo "  python api/app.py"
echo ""
echo "Le serveur sera accessible sur :"
echo "  - Local: http://localhost:5000"
echo "  - Réseau: http://192.168.1.116:5000"
