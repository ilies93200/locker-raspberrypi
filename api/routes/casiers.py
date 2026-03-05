from flask import Blueprint, request, jsonify
from api.models import db, Casier
from api.utils.gpio_controller import locker

bp = Blueprint('casiers', __name__, url_prefix='/api/casiers')

@bp.route('', methods=['GET'])
def get_casiers():
    """Récupérer l'état du casier"""
    casier = Casier.query.get(1)
    
    if not casier:
        return jsonify({'error': 'Casier non trouvé'}), 404
    
    return jsonify(casier.to_dict()), 200

@bp.route('/1/ouvrir', methods=['POST'])
def ouvrir_casier():
    """Ouvrir le casier (pour tests)"""
    data = request.get_json() or {}
    duree = data.get('duree', 5)
    
    success = locker.ouvrir_casier(duree=duree)
    
    if success:
        return jsonify({'message': f'Casier ouvert pendant {duree} secondes'}), 200
    else:
        return jsonify({'error': 'Erreur lors de l\'ouverture du casier'}), 500

@bp.route('/1/etat', methods=['GET'])
def get_etat_casier():
    """Récupérer l'état physique du casier (GPIO)"""
    etat = locker.get_etat()
    casier = Casier.query.get(1)
    
    return jsonify({
        'etat_physique': etat,
        'etat_logique': casier.etat if casier else 'inconnu'
    }), 200
