from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Livreur(db.Model):
    __tablename__ = 'livreurs'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    adresse = db.Column(db.String(200))
    login = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_login = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'prenom': self.prenom,
            'adresse': self.adresse,
            'login': self.login,
            'first_login': self.first_login
        }

class Commercant(db.Model):
    __tablename__ = 'commercants'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    adresse = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100))
    telephone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'adresse': self.adresse,
            'email': self.email,
            'telephone': self.telephone
        }

class Casier(db.Model):
    __tablename__ = 'casier'
    
    id = db.Column(db.Integer, primary_key=True, default=1)
    taille = db.Column(db.String(10), nullable=False, default='M')
    etat = db.Column(db.String(20), default='libre')
    gpio_pin = db.Column(db.Integer, default=17)
    
    def to_dict(self):
        return {
            'id': self.id,
            'taille': self.taille,
            'etat': self.etat,
            'gpio_pin': self.gpio_pin
        }

class Commande(db.Model):
    __tablename__ = 'commandes'
    
    id = db.Column(db.Integer, primary_key=True)
    email_client = db.Column(db.String(100), nullable=False)
    taille_casier = db.Column(db.String(10), nullable=False)
    poids = db.Column(db.Float)
    commercant_id = db.Column(db.Integer, db.ForeignKey('commercants.id'))
    livreur_id = db.Column(db.Integer, db.ForeignKey('livreurs.id'))
    casier_id = db.Column(db.Integer, db.ForeignKey('casier.id'), default=1)
    code_commande = db.Column(db.String(50), unique=True)
    mot_de_passe = db.Column(db.String(20))
    statut = db.Column(db.String(50), default='créée')
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    date_recuperation_livreur = db.Column(db.DateTime)
    date_depot = db.Column(db.DateTime)
    date_retrait = db.Column(db.DateTime)
    
    commercant = db.relationship('Commercant', backref='commandes')
    livreur = db.relationship('Livreur', backref='commandes')
    casier = db.relationship('Casier', backref='commandes')
    
    def to_dict(self):
        return {
            'id': self.id,
            'email_client': self.email_client,
            'taille_casier': self.taille_casier,
            'poids': self.poids,
            'commercant': self.commercant.to_dict() if self.commercant else None,
            'livreur': self.livreur.to_dict() if self.livreur else None,
            'code_commande': self.code_commande,
            'statut': self.statut,
            'date_creation': self.date_creation.isoformat() if self.date_creation else None,
            'date_depot': self.date_depot.isoformat() if self.date_depot else None,
            'date_retrait': self.date_retrait.isoformat() if self.date_retrait else None
        }
