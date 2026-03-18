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
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                ${commandes.map(c => `
                    <tr>
                        <td>${c.email_client}</td>
                        <td>${c.taille_casier}</td>
                        <td>${c.poids ? c.poids + ' kg' : '-'}</td>
                        <td>
                            <button onclick="deposerCommande(${c.id})" class="btn btn-info">
                                Déposer dans le casier
                            </button>
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

📋 INFORMATIONS CLIENT :
━━━━━━━━━━━━━━━━━━━━━━━━━━
🔑 Code Commande: ${data.code_commande}
🔐 Mot de Passe: ${data.mot_de_passe}

💡 Ces informations sont à communiquer au client pour le retrait.
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

chargerCommandes();

setInterval(chargerCommandes, 10000);
