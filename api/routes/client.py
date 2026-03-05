from flask import Blueprint, request, jsonify
from api.models import db, Commande, Casier
from api.utils.gpio_controller import locker
from datetime import datetime

bp = Blueprint('client', __name__, url_prefix='/api/client')

@bp.route('/retirer', methods=['POST'])
def retirer_commande():
    """Retirer une commande du casier (interface client kiosk)"""
    data = request.get_json()
    code_commande = data.get('code_commande')
    mot_de_passe = data.get('mot_de_passe')
    
    if not code_commande or not mot_de_passe:
        return jsonify({'error': 'Code de commande et mot de passe requis'}), 400
    
    commande = Commande.query.filter_by(code_commande=code_commande).first()
    
    if not commande:
        return jsonify({'error': 'Numéro de commande inexistant'}), 404
    
    if commande.statut != 'déposée':
        return jsonify({'error': 'Cette commande n\'est pas disponible'}), 400
    
    if commande.mot_de_passe != mot_de_passe:
        return jsonify({'error': 'Mot de passe incorrect'}), 401
    
    casier = Casier.query.get(1)
    if not casier or casier.etat != 'occupé':
        return jsonify({'error': 'Le casier est vide'}), 400
    
    locker.ouvrir_casier(duree=5)
    
    commande.statut = 'récupérée_par_client'
    commande.date_retrait = datetime.utcnow()
    casier.etat = 'libre'
    
    db.session.commit()
    
    return jsonify({
        'message': 'Casier ouvert ! Récupérez votre colis.',
        'commande': commande.to_dict()
    }), 200
