from flask import Blueprint, request, jsonify
from api.models import db, Commande, Casier
from api.utils.gpio_controller import locker
from datetime import datetime

bp = Blueprint('client', __name__, url_prefix='/api/client')

@bp.route('/retirer', methods=['POST'])
def retirer_commande():
    """Retirer une commande du casier (interface client kiosk)"""
    data = request.get_json()
    code_retrait = data.get('code_retrait')
    
    if not code_retrait:
        return jsonify({'error': 'Code de retrait requis'}), 400
    
    commande = Commande.query.filter_by(code_commande=code_retrait).first()
    
    if not commande:
        return jsonify({'error': 'Code de retrait invalide'}), 404
    
    if commande.statut != 'déposée':
        return jsonify({'error': 'Cette commande n\'est pas disponible'}), 400
    
    casier = Casier.query.get(1)
    if not casier or casier.etat != 'occupé':
        return jsonify({'error': 'Le casier est vide'}), 400
    
    locker.ouvrir_casier(duree=2)
    
    commande.statut = 'récupérée_par_client'
    commande.date_retrait = datetime.utcnow()
    casier.etat = 'libre'
    
    db.session.commit()
    
    return jsonify({
        'message': 'Casier ouvert ! Récupérez votre colis.',
        'commande': commande.to_dict()
    }), 200
