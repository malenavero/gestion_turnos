// turnos/static/js/ui_funciones.js

// Error message function
function closeErrorMessage() {
    document.getElementById('errorMessage').style.display = 'none';
}

// Close Alert
function closeAlert(idAlert) {
    document.getElementById(idAlert).style.display = 'none';
}

function toggleEspecialidad() {
    const medicoSelect = document.getElementById('medico');
    const especialidadSelect = document.getElementById('especialidad');

    // Si hay un médico seleccionado, deshabilitar especialidad
    if (medicoSelect.value) {
        especialidadSelect.disabled = true;
    } else {
        especialidadSelect.disabled = false;
    }
}

function toggleMedico() {
    const especialidadSelect = document.getElementById('especialidad');
    const medicoSelect = document.getElementById('medico');

    // Si hay una especialidad seleccionada, deshabilitar médico
    if (especialidadSelect.value) {
        medicoSelect.disabled = true;
    } else {
        medicoSelect.disabled = false; // Habilitar si no hay especialidad seleccionada
    }
}
