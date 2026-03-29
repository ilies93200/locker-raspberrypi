from flask import Flask, render_template, send_from_directory
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from api.config import Config
from api.models import db
from api.utils.locker_kiosk import init_kiosk, get_kiosk
import os

app = Flask(__name__, 
            template_folder='../web',
            static_folder='../web/static')
app.config.from_object(Config)

CORS(app)
db.init_app(app)
jwt = JWTManager(app)

from api.routes import auth, commandes, livreurs, casiers, client

app.register_blueprint(auth.bp)
app.register_blueprint(commandes.bp)
app.register_blueprint(livreurs.bp)
app.register_blueprint(casiers.bp)
app.register_blueprint(client.bp)

# Initialiser le kiosk avec clavier
init_kiosk(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/commercant')
def commercant():
    return render_template('commercant/index.html')

@app.route('/livreur')
def livreur():
    return render_template('livreur/login.html')

@app.route('/livreur/change-password')
def livreur_change_password():
    return render_template('livreur/change-password.html')

@app.route('/livreur/dashboard')
def livreur_dashboard():
    return render_template('livreur/dashboard.html')

@app.route('/client')
def client_kiosk():
    return render_template('client/index.html')

with app.app_context():
    db.create_all()
    print("✅ Base de données initialisée")
    
    # Démarrer le kiosk uniquement dans le processus principal
    # (éviter le double démarrage en mode debug Flask)
    import os
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true' or not app.debug:
        kiosk = get_kiosk()
        kiosk.start()
        print("✅ Kiosk client actif - Clavier en écoute")

if __name__ == '__main__':
    print("🚀 Démarrage du serveur Locker...")
    print(f"📍 Accès local: http://localhost:5000")
    print(f"📍 Accès réseau: http://192.168.1.116:5000")
    print(f"   - IHM Commerçant: http://192.168.1.116:5000/commercant")
    print(f"   - App Livreur: http://192.168.1.116:5000/livreur")
    print(f"   - Client Kiosk: http://192.168.1.116:5000/client")
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
