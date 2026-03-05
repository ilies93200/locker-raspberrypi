from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.models import db, Commande, Casier, Commercant
from api.utils.email_sender import envoyer_email_client
from api.utils.gpio_controller import locker
from datetime import datetime
import random
import string

bp = Blueprint('commandes', __name__, url_prefix='/api/commandes')

def generer_code_commande():
    """Génère un code de commande unique (ex: CMD-20240312-0042)"""
    date_str = datetime.now().strftime('%Y%m%d')
    random_num = random.randint(1000, 9999)
    return f"CMD-{date_str}-{random_num}"

def generer_mot_de_passe():
    """Génère un mot de passe aléatoire (ex: 7K3mP9)"""
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(6))

@bp.route('', methods=['GET'])
def get_commandes():
    """Récupérer toutes les commandes"""
    commandes = Commande.query.all()
    return jsonify([c.to_dict() for c in commandes]), 200

@bp.route('', methods=['POST'])
def create_commande():
    """Créer une nouvelle commande"""
    data = request.get_json()
    
    required_fields = ['email_client', 'taille_casier', 'commercant_id']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'Le champ {field} est requis'}), 400
    
    commercant = Commercant.query.get(data['commercant_id'])
    if not commercant:
        return jsonify({'error': 'Commerçant non trouvé'}), 404
    
    commande = Commande(
        email_client=data['email_client'],
        taille_casier=data['taille_casier'],
        poids=data.get('poids'),
        commercant_id=data['commercant_id']
    )
    
    db.session.add(commande)
    db.session.commit()
    
    return jsonify(commande.to_dict()), 201

@bp.route('/<int:id>/certifier', methods=['POST'])
def certifier_recuperation(id):
    """Certifier qu'un livreur a récupéré la commande chez le commerçant"""
    data = request.get_json()
    livreur_id = data.get('livreur_id')
    
    if not livreur_id:
        return jsonify({'error': 'ID du livreur requis'}), 400
    
    commande = Commande.query.get(id)
    if not commande:
        return jsonify({'error': 'Commande non trouvée'}), 404
    
    if commande.statut != 'créée':
        return jsonify({'error': 'Cette commande a déjà été récupérée'}), 400
    
    commande.livreur_id = livreur_id
    commande.statut = 'récupérée_par_livreur'
    commande.date_recuperation_livreur = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify(commande.to_dict()), 200

@bp.route('/<int:id>/deposer', methods=['POST'])
@jwt_required()
def deposer_commande(id):
    """Déposer une commande dans le casier (action du livreur)"""
    livreur_id = get_jwt_identity()
    
    commande = Commande.query.get(id)
    if not commande:
        return jsonify({'error': 'Commande non trouvée'}), 404
    
    if commande.livreur_id != livreur_id:
        return jsonify({'error': 'Cette commande n\'est pas assignée à ce livreur'}), 403
    
    if commande.statut != 'récupérée_par_livreur':
        return jsonify({'error': 'Cette commande n\'a pas été récupérée'}), 400
    
    casier = Casier.query.get(1)
    if casier.etat != 'libre':
        return jsonify({'error': 'Le casier est déjà occupé'}), 400
    
    code_commande = generer_code_commande()
    mot_de_passe = generer_mot_de_passe()
    
    commande.code_commande = code_commande
    commande.mot_de_passe = mot_de_passe
    commande.statut = 'déposée'
    commande.date_depot = datetime.utcnow()
    
    casier.etat = 'occupé'
    
    locker.ouvrir_casier(duree=5)
    
    envoyer_email_client(commande.email_client, code_commande, mot_de_passe)
    
    db.session.commit()
    
    return jsonify({
        'message': 'Commande déposée avec succès',
        'commande': commande.to_dict()
    }), 200

@bp.route('/<int:id>', methods=['DELETE'])
def delete_commande(id):
    """Supprimer une commande"""
    commande = Commande.query.get(id)
    
    if not commande:
        return jsonify({'error': 'Commande non trouvée'}), 404
    
    if commande.statut == 'déposée':
        casier = Casier.query.get(1)
        casier.etat = 'libre'
    
    db.session.delete(commande)
    db.session.commit()
    
    return jsonify({'message': 'Commande supprimée avec succès'}), 200

@bp.route('/livreur/disponibles', methods=['GET'])
@jwt_required()
def get_commandes_disponibles():
    """Récupérer les commandes disponibles pour le livreur connecté"""
    livreur_id = get_jwt_identity()
    
    commandes = Commande.query.filter(
        (Commande.statut == 'créée') | 
        ((Commande.statut == 'récupérée_par_livreur') & (Commande.livreur_id == livreur_id))
    ).all()
    
    return jsonify([c.to_dict() for c in commandes]), 200
