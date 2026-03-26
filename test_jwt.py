import sys
sys.path.insert(0, '/root/locker-raspberrypi')
from api.app import app
from api.models import db, Livreur
import bcrypt

with app.app_context():
    livreur = Livreur.query.first()
    if livreur:
        print('Livreur ID:', livreur.id)
        print('Livreur login:', livreur.login)
        print('Livreur first_login:', livreur.first_login)
    else:
        print('Aucun livreur trouvé')
