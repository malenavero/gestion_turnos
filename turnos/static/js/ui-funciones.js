// turnos/static/js/ui_funciones.js

// Modal functions
function openModal(title, message, actionUrl) {
    document.getElementById('modalTitle').textContent = title;
    document.getElementById('modalMessage').textContent = message;
    document.getElementById('modalForm').action = actionUrl;
    document.getElementById('confirmationModal').style.display = 'block';
}

function closeModal() {
    document.getElementById('confirmationModal').style.display = 'none';
}

// Error message function
function closeErrorMessage() {
    document.getElementById('errorMessage').style.display = 'none';
}
