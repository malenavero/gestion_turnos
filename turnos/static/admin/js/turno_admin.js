// turnos/static/admin/js/turno_admin.js
document.addEventListener('DOMContentLoaded', function() {
    // Updatea el estado automaticamente cuando se selecciona un paciente
    const pacienteField = document.getElementById('id_paciente');
    const estadoField = document.getElementById('id_estado');

    function updateEstado() {
        if (pacienteField.value) {
            estadoField.value = 'ocupado';
        } else {
            estadoField.value = 'disponible';
        }
    }

    pacienteField.addEventListener('change', function() {
        updateEstado();
    });

    updateEstado();
});
