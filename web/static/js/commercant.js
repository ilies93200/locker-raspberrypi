const alertDiv = document.getElementById('alert');

function showAlert(message, type) {
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    alertDiv.style.display = 'block';
    
    setTimeout(() => {
        alertDiv.style.display = 'none';
    }, 5000);
}

document.getElementById('livreurForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const data = {
        nom: document.getElementById('nom').value,
        prenom: document.getElementById('prenom').value,
        adresse: document.getElementById('adresse').value,
        login: document.getElementById('login').value,
        password: document.getElementById('password').value
    };
    
    try {
        const response = await fetch('/api/livreurs', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showAlert('✅ Livreur créé avec succès', 'success');
            e.target.reset();
            chargerLivreurs();
        } else {
            showAlert('❌ ' + result.error, 'error');
        }
    } catch (error) {
        showAlert('❌ Erreur de connexion', 'error');
    }
});

document.getElementById('commandeForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const data = {
        email_client: document.getElementById('email_client').value,
        taille_casier: document.getElementById('taille_casier').value,
        poids: parseFloat(document.getElementById('poids').value) || null,
        commercant_id: 1
    };
    
    try {
        const response = await fetch('/api/commandes', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showAlert('✅ Commande créée avec succès', 'success');
            e.target.reset();
            chargerCommandes();
        } else {
            showAlert('❌ ' + result.error, 'error');
        }
    } catch (error) {
        showAlert('❌ Erreur de connexion', 'error');
    }
});

async function chargerLivreurs() {
    try {
        const response = await fetch('/api/livreurs');
        const livreurs = await response.json();
        
        const html = livreurs.length > 0 ? `
            <table>
                <thead>
                    <tr>
                        <th>Nom</th>
                        <th>Prénom</th>
                        <th>Login</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    ${livreurs.map(l => `
                        <tr>
                            <td>${l.nom}</td>
                            <td>${l.prenom}</td>
                            <td>${l.login}</td>
                            <td>
                                <button onclick="supprimerLivreur(${l.id})" class="btn btn-danger">
                                    Supprimer
                                </button>
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        ` : '<p>Aucun livreur enregistré</p>';
        
        document.getElementById('livreursList').innerHTML = html;
    } catch (error) {
        console.error('Erreur:', error);
    }
}

async function supprimerLivreur(id) {
    if (!confirm('Voulez-vous vraiment supprimer ce livreur ?')) return;
    
    try {
        const response = await fetch(`/api/livreurs/${id}`, { method: 'DELETE' });
        
        if (response.ok) {
            showAlert('✅ Livreur supprimé', 'success');
            chargerLivreurs();
        } else {
            showAlert('❌ Erreur lors de la suppression', 'error');
        }
    } catch (error) {
        showAlert('❌ Erreur de connexion', 'error');
    }
}

async function chargerCommandes() {
    try {
        const response = await fetch('/api/commandes');
        const commandes = await response.json();
        
        const html = commandes.length > 0 ? `
            <table>
                <thead>
                    <tr>
                        <th>Email Client</th>
                        <th>Taille</th>
                        <th>Livreur</th>
                        <th>Statut</th>
                        <th>Code Retrait</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    ${commandes.map(c => `
                        <tr>
                            <td>${c.email_client}</td>
                            <td>${c.taille_casier}</td>
                            <td>${c.livreur ? `${c.livreur.prenom} ${c.livreur.nom}` : '-'}</td>
                            <td><span class="badge badge-${getStatutClass(c.statut)}">${c.statut}</span></td>
                            <td><strong style="font-size: 16px; letter-spacing: 2px;">${c.code_commande || '-'}</strong></td>
                            <td>
                                ${c.statut === 'créée' ? `
                                    <button onclick="certifierCommande(${c.id})" class="btn btn-success">
                                        Certifier
                                    </button>
                                ` : ''}
                                ${c.statut === 'déposée' ? `
                                    <button onclick="afficherInfosRetrait(${c.id})" class="btn btn-info">
                                        Infos Retrait
                                    </button>
                                ` : ''}
                                ${c.statut !== 'récupérée_par_client' ? `
                                    <button onclick="supprimerCommande(${c.id})" class="btn btn-danger">
                                        Supprimer
                                    </button>
                                ` : ''}
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        ` : '<p>Aucune commande</p>';
        
        document.getElementById('commandesList').innerHTML = html;
    } catch (error) {
        console.error('Erreur:', error);
    }
}

function getStatutClass(statut) {
    const classes = {
        'créée': 'info',
        'récupérée_par_livreur': 'warning',
        'déposée': 'success',
        'récupérée_par_client': 'success'
    };
    return classes[statut] || 'info';
}

async function certifierCommande(id) {
    const livreurs = await fetch('/api/livreurs').then(r => r.json());
    
    if (livreurs.length === 0) {
        showAlert('❌ Aucun livreur disponible', 'error');
        return;
    }
    
    const livreurId = prompt(`ID du livreur (${livreurs.map(l => `${l.id}: ${l.nom} ${l.prenom}`).join(', ')}):`);
    
    if (!livreurId) return;
    
    try {
        const response = await fetch(`/api/commandes/${id}/certifier`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ livreur_id: parseInt(livreurId) })
        });
        
        if (response.ok) {
            showAlert('✅ Commande certifiée', 'success');
            chargerCommandes();
        } else {
            const result = await response.json();
            showAlert('❌ ' + result.error, 'error');
        }
    } catch (error) {
        showAlert('❌ Erreur de connexion', 'error');
    }
}

async function supprimerCommande(id) {
    if (!confirm('Voulez-vous vraiment supprimer cette commande ?')) return;
    
    try {
        const response = await fetch(`/api/commandes/${id}`, { method: 'DELETE' });
        
        if (response.ok) {
            showAlert('✅ Commande supprimée', 'success');
            chargerCommandes();
            rafraichirCasier();
        } else {
            showAlert('❌ Erreur lors de la suppression', 'error');
        }
    } catch (error) {
        showAlert('❌ Erreur de connexion', 'error');
    }
}

async function rafraichirCasier() {
    try {
        const response = await fetch('/api/casiers');
        const casier = await response.json();
        
        const html = `
            <div style="padding: 20px; background: #f7fafc; border-radius: 8px;">
                <p><strong>Taille:</strong> ${casier.taille}</p>
                <p><strong>État:</strong> <span class="badge badge-${casier.etat === 'libre' ? 'success' : 'warning'}">${casier.etat}</span></p>
                <p><strong>GPIO Pin:</strong> ${casier.gpio_pin}</p>
            </div>
        `;
        
        document.getElementById('casierEtat').innerHTML = html;
    } catch (error) {
        console.error('Erreur:', error);
    }
}

chargerLivreurs();
chargerCommandes();
rafraichirCasier();

async function afficherInfosRetrait(id) {
    try {
        const response = await fetch(`/api/commandes/${id}`);
        const commande = await response.json();
        
        const message = `
📦 CODE DE RETRAIT
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

setInterval(() => {
    chargerCommandes();
    rafraichirCasier();
}, 10000);
