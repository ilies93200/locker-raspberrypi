-- Schéma de base de données pour le système de locker
-- Projet BTS/Lycée - Casier de livraison intelligent
-- Version: 1.0 (1 casier unique)

-- Table des livreurs
CREATE TABLE IF NOT EXISTS livreurs (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    nom         TEXT NOT NULL,
    prenom      TEXT NOT NULL,
    adresse     TEXT,
    login       TEXT UNIQUE NOT NULL,
    password    TEXT NOT NULL,         -- hashé avec bcrypt
    first_login BOOLEAN DEFAULT 1,     -- 1 = doit changer son mot de passe
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Table des commerçants
CREATE TABLE IF NOT EXISTS commercants (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    nom     TEXT NOT NULL,
    adresse TEXT NOT NULL,
    email   TEXT,
    telephone TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Table du casier (1 seul casier)
CREATE TABLE IF NOT EXISTS casier (
    id      INTEGER PRIMARY KEY DEFAULT 1,
    taille  TEXT NOT NULL DEFAULT 'M',     -- S, M, L, XL
    etat    TEXT DEFAULT 'libre',          -- libre, occupé
    gpio_pin INTEGER DEFAULT 17,           -- GPIO 17
    CHECK (id = 1)                         -- Force un seul casier
);

-- Table des commandes
CREATE TABLE IF NOT EXISTS commandes (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    email_client    TEXT NOT NULL,
    taille_casier   TEXT NOT NULL,         -- S, M, L, XL
    poids           REAL,
    commercant_id   INTEGER REFERENCES commercants(id),
    livreur_id      INTEGER REFERENCES livreurs(id),
    casier_id       INTEGER DEFAULT 1 REFERENCES casier(id),
    code_commande   TEXT UNIQUE,           -- généré automatiquement (ex: CMD-20240312-0042)
    mot_de_passe    TEXT,                  -- généré automatiquement (ex: 7K3mP9)
    statut          TEXT DEFAULT 'créée',
    -- Statuts possibles:
    --   'créée' → commande créée par le commerçant
    --   'récupérée_par_livreur' → livreur a récupéré le colis chez le commerçant
    --   'déposée' → colis déposé dans le casier
    --   'récupérée_par_client' → client a récupéré son colis
    date_creation   DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_recuperation_livreur DATETIME,
    date_depot      DATETIME,
    date_retrait    DATETIME
);

-- Insertion du casier unique
INSERT OR IGNORE INTO casier (id, taille, etat, gpio_pin) 
VALUES (1, 'M', 'libre', 17);

-- Insertion d'un commerçant par défaut (pour les tests)
INSERT OR IGNORE INTO commercants (id, nom, adresse, email, telephone)
VALUES (1, 'Boutique Test', '123 Rue du Centre-Ville', 'boutique@test.fr', '0123456789');

-- Index pour optimiser les recherches
CREATE INDEX IF NOT EXISTS idx_commandes_statut ON commandes(statut);
CREATE INDEX IF NOT EXISTS idx_commandes_code ON commandes(code_commande);
CREATE INDEX IF NOT EXISTS idx_livreurs_login ON livreurs(login);
