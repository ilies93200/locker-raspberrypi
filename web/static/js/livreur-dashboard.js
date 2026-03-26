const token = localStorage.getItem('token');
const livreur = JSON.parse(localStorage.getItem('livreur') || '{}');

if (!token) {
    window.location.href = '/livreur/login.html';
}

document.getElementById('welcomeMessage').textContent = 
    `Bienvenue ${livreur.prenom} ${livreur.nom}`;

const alertDiv = document.getElementById('alert');

function showAlert(message, type) {
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    alertDiv.style.display = 'block';
    
    setTimeout(() => {
        alertDiv.style.display = 'none';
    }, 5000);
}

function deconnexion() {
    localStorage.removeItem('token');
    localStorage.removeItem('livreur');
    window.location.href = '/livreur/login.html';
}

async function chargerCommandes() {
    try {
        const response = await fetch('/api/commandes/livreur/disponibles', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.status === 401) {
            deconnexion();
            return;
        }
        
        const commandes = await response.json();
        
        const disponibles = commandes.filter(c => c.statut === 'créée');
        const recuperees = commandes.filter(c => c.statut === 'récupérée_par_livreur');
        
        afficherCommandesDisponibles(disponibles);
        afficherCommandesRecuperees(recuperees);
        
    } catch (error) {
        console.error('Erreur:', error);
        showAlert('❌ Erreur de chargement des commandes', 'error');
    }
}

function afficherCommandesDisponibles(commandes) {
    const html = commandes.length > 0 ? `
        <table>
            <thead>
                <tr>
                    <th>Commerçant</th>
                    <th>Adresse</th>
                    <th>Taille</th>
                    <th>Poids</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                ${commandes.map(c => `
                    <tr>
                        <td>${c.commercant?.nom || '-'}</td>
                        <td>${c.commercant?.adresse || '-'}</td>
                        <td>${c.taille_casier}</td>
                        <td>${c.poids ? c.poids + ' kg' : '-'}</td>
                        <td>
                            <button onclick="recupererCommande(${c.id})" class="btn btn-success">
                                Récupérer
                            </button>
                        </td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    ` : '<p>Aucune commande disponible</p>';
    
    document.getElementById('commandesDisponibles').innerHTML = html;
}

function afficherCommandesRecuperees(commandes) {
    const html = commandes.length > 0 ? `
        <table>
            <thead>
                <tr>
                    <th>Email Client</th>
                    <th>Taille</th>
                    <th>Poids</th>
                    <th>Code Retrait</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                ${commandes.map(c => `
                    <tr>
                        <td>${c.email_client}</td>
                        <td>${c.taille_casier}</td>
                        <td>${c.poids ? c.poids + ' kg' : '-'}</td>
                        <td><strong style="font-size: 18px; letter-spacing: 2px;">${c.code_commande || '-'}</strong></td>
                        <td>
                            ${!c.code_commande || c.code_commande.startsWith('CMD-') ? `
                                <button onclick="deposerCommande(${c.id})" class="btn btn-info">
                                    Déposer dans le casier
                                </button>
                            ` : `
                                <button onclick="afficherInfosClient(${c.id})" class="btn btn-success">
                                    Voir Code Client
                                </button>
                            `}
                        </td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    ` : '<p>Aucune commande récupérée</p>';
    
    document.getElementById('commandesRecuperees').innerHTML = html;
}

async function recupererCommande(id) {
    if (!confirm('Avez-vous récupéré ce colis chez le commerçant ?')) return;
    
    try {
        const response = await fetch(`/api/commandes/${id}/certifier`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ livreur_id: livreur.id })
        });
        
        if (response.ok) {
            showAlert('✅ Commande récupérée avec succès', 'success');
            chargerCommandes();
        } else {
            const data = await response.json();
            showAlert('❌ ' + data.error, 'error');
        }
    } catch (error) {
        showAlert('❌ Erreur de connexion', 'error');
    }
}

async function deposerCommande(id) {
    if (!confirm('Êtes-vous prêt à déposer le colis dans le casier ? Le casier va s\'ouvrir automatiquement.')) return;
    
    try {
        const response = await fetch(`/api/commandes/${id}/deposer`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (response.ok) {
            const message = `
✅ Commande déposée avec succès !

🔓 Le casier est ouvert, déposez le colis maintenant.

📋 CODE DE RETRAIT CLIENT :
━━━━━━━━━━━━━━━━━━━━━━━━━━
🔑 ${data.code_retrait}

💡 Ce code est à communiquer au client pour le retrait.
(8 caractères: chiffres 0-9 et lettres A-D)
            `;
            alert(message);
            showAlert('✅ Commande déposée avec succès', 'success');
            chargerCommandes();
        } else {
            showAlert('❌ ' + data.error, 'error');
        }
    } catch (error) {
        showAlert('❌ Erreur de connexion', 'error');
    }
}

async function afficherInfosClient(id) {
    try {
        const response = await fetch(`/api/commandes/${id}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        const commande = await response.json();
        
        const message = `
📦 CODE DE RETRAIT CLIENT
━━━━━━━━━━━━━━━━━━━━━━━━━━

👤 Client: ${commande.email_client}
🔑 Code: ${commande.code_commande}

📱 À communiquer au client pour le retrait
(8 caractères: chiffres 0-9 et lettres A-D)
        `;
        
        alert(message);
    } catch (error) {
        showAlert('❌ Erreur lors de la récupération des infos', 'error');
    }
}

chargerCommandes();

setInterval(chargerCommandes, 10000);
