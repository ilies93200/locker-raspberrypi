from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from api.models import db, Livreur
import bcrypt

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/login', methods=['POST'])
def login():
    """Connexion d'un livreur"""
    data = request.get_json()
    login = data.get('login')
    password = data.get('password')
    
    if not login or not password:
        return jsonify({'error': 'Login et mot de passe requis'}), 400
    
    livreur = Livreur.query.filter_by(login=login).first()
    
    if not livreur:
        return jsonify({'error': 'Login ou mot de passe incorrect'}), 401
    
    if not bcrypt.checkpw(password.encode('utf-8'), livreur.password.encode('utf-8')):
        return jsonify({'error': 'Login ou mot de passe incorrect'}), 401
    
    access_token = create_access_token(identity=str(livreur.id))
    
    return jsonify({
        'access_token': access_token,
        'livreur': livreur.to_dict(),
        'first_login': livreur.first_login
    }), 200

@bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """Changer le mot de passe (obligatoire au premier login)"""
    livreur_id = int(get_jwt_identity())
    data = request.get_json()
    new_password = data.get('new_password')
    
    if not new_password or len(new_password) < 6:
        return jsonify({'error': 'Le mot de passe doit contenir au moins 6 caractères'}), 400
    
    livreur = Livreur.query.get(livreur_id)
    if not livreur:
        return jsonify({'error': 'Livreur non trouvé'}), 404
    
    hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
    livreur.password = hashed.decode('utf-8')
    livreur.first_login = False
    
    db.session.commit()
    
    return jsonify({'message': 'Mot de passe changé avec succès'}), 200

@bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Récupérer les infos du livreur connecté"""
    livreur_id = int(get_jwt_identity())
    livreur = Livreur.query.get(livreur_id)
    
    if not livreur:
        return jsonify({'error': 'Livreur non trouvé'}), 404
    
    return jsonify(livreur.to_dict()), 200
