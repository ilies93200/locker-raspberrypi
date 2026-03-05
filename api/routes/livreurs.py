from flask import Blueprint, request, jsonify
from api.models import db, Livreur
import bcrypt

bp = Blueprint('livreurs', __name__, url_prefix='/api/livreurs')

@bp.route('', methods=['GET'])
def get_livreurs():
    """Récupérer tous les livreurs"""
    livreurs = Livreur.query.all()
    return jsonify([l.to_dict() for l in livreurs]), 200

@bp.route('', methods=['POST'])
def create_livreur():
    """Créer un nouveau livreur"""
    data = request.get_json()
    
    required_fields = ['nom', 'prenom', 'login', 'password']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'Le champ {field} est requis'}), 400
    
    if Livreur.query.filter_by(login=data['login']).first():
        return jsonify({'error': 'Ce login existe déjà'}), 400
    
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    
    livreur = Livreur(
        nom=data['nom'],
        prenom=data['prenom'],
        adresse=data.get('adresse', ''),
        login=data['login'],
        password=hashed_password.decode('utf-8'),
        first_login=True
    )
    
    db.session.add(livreur)
    db.session.commit()
    
    return jsonify(livreur.to_dict()), 201

@bp.route('/<int:id>', methods=['DELETE'])
def delete_livreur(id):
    """Supprimer un livreur"""
    livreur = Livreur.query.get(id)
    
    if not livreur:
        return jsonify({'error': 'Livreur non trouvé'}), 404
    
    db.session.delete(livreur)
    db.session.commit()
    
    return jsonify({'message': 'Livreur supprimé avec succès'}), 200

@bp.route('/<int:id>', methods=['GET'])
def get_livreur(id):
    """Récupérer un livreur par son ID"""
    livreur = Livreur.query.get(id)
    
    if not livreur:
        return jsonify({'error': 'Livreur non trouvé'}), 404
    
    return jsonify(livreur.to_dict()), 200
