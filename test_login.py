import sys
sys.path.insert(0, '/root/locker-raspberrypi')
from api.app import app
from api.models import db, Livreur
from flask_jwt_extended import create_access_token
import bcrypt

with app.app_context():
    # Récupérer le livreur
    livreur = Livreur.query.filter_by(login='ilies').first()
    
    if livreur:
        # Créer un token
        token = create_access_token(identity=livreur.id)
        print('Token généré:', token)
        
        # Vérifier le mot de passe
        test_password = 'ilies'
        if bcrypt.checkpw(test_password.encode('utf-8'), livreur.password.encode('utf-8')):
            print('Mot de passe correct')
        else:
            print('Mot de passe incorrect')
            # Réinitialiser le mot de passe
            hashed = bcrypt.hashpw(test_password.encode('utf-8'), bcrypt.gensalt())
            livreur.password = hashed.decode('utf-8')
            livreur.first_login = False
            db.session.commit()
            print('Mot de passe réinitialisé à: ilies')
    else:
        print('Livreur non trouvé')
