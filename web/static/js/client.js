const form = document.getElementById('retraitForm');
const alertDiv = document.getElementById('alert');

function showAlert(message, type) {
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    alertDiv.style.display = 'block';
    
    setTimeout(() => {
        alertDiv.style.display = 'none';
    }, 5000);
}

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const code_retrait = document.getElementById('code_retrait').value.trim().toUpperCase();
    
    if (code_retrait.length !== 8) {
        showAlert('❌ Le code doit contenir 8 caractères', 'error');
        return;
    }
    
    try {
        const response = await fetch('/api/client/retirer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ code_retrait })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showAlert('✅ ' + data.message, 'success');
            form.reset();
        } else {
            showAlert('❌ ' + data.error, 'error');
        }
    } catch (error) {
        showAlert('❌ Erreur de connexion au serveur', 'error');
        console.error('Erreur:', error);
    }
});
