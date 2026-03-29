const alertDiv = document.getElementById('alert');
const codeDisplay = document.getElementById('codeDisplay');
const statusBox = document.getElementById('statusBox');
const btnErase = document.getElementById('btnErase');
const btnValidate = document.getElementById('btnValidate');

let currentBuffer = '';

// Mettre à jour l'affichage du code
function updateDisplay(buffer) {
    currentBuffer = buffer;
    
    if (buffer.length === 0) {
        codeDisplay.textContent = '________';
        codeDisplay.classList.add('empty');
    } else {
        // Afficher le code + underscores pour compléter à 8
        const display = buffer + '_'.repeat(8 - buffer.length);
        codeDisplay.textContent = display;
        codeDisplay.classList.remove('empty');
    }
}

// Afficher un message de statut
function showStatus(message, type) {
    statusBox.textContent = message;
    statusBox.className = 'status ' + type;
    statusBox.style.display = 'block';
    
    if (type === 'success') {
        setTimeout(() => {
            statusBox.style.display = 'none';
        }, 5000);
    }
}

// Récupérer le buffer du clavier en temps réel
async function fetchBuffer() {
    try {
        const response = await fetch('/api/client/kiosk/status');
        const data = await response.json();
        
        if (data.buffer !== currentBuffer) {
            updateDisplay(data.buffer);
        }
        
        // Vérifier si un code a été validé
        if (data.last_result) {
            if (data.last_result.success) {
                showStatus('✅ ' + data.last_result.message, 'success');
            } else {
                showStatus('❌ ' + data.last_result.message, 'error');
            }
        }
    } catch (error) {
        console.error('Erreur récupération buffer:', error);
    }
}

// Effacer le buffer
async function clearBuffer() {
    try {
        await fetch('/api/client/kiosk/clear', { method: 'POST' });
        updateDisplay('');
        statusBox.style.display = 'none';
    } catch (error) {
        console.error('Erreur effacement:', error);
    }
}

// Valider le code
async function validateCode() {
    if (currentBuffer.length === 0) {
        showStatus('❌ Veuillez entrer un code', 'error');
        return;
    }
    
    try {
        const response = await fetch('/api/client/retirer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ code_retrait: currentBuffer })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showStatus('✅ ' + data.message, 'success');
            clearBuffer();
        } else {
            showStatus('❌ ' + data.error, 'error');
        }
    } catch (error) {
        showStatus('❌ Erreur de connexion', 'error');
        console.error('Erreur:', error);
    }
}

// Boutons
btnErase.addEventListener('click', clearBuffer);
btnValidate.addEventListener('click', validateCode);

// Mettre à jour le buffer toutes les 500ms
setInterval(fetchBuffer, 500);

// Première mise à jour immédiate
fetchBuffer();
