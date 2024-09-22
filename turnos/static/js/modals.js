// Función para abrir el Modal de Confirmación
function openConfirmacionModal(titulo, mensaje, urlAccion) {
    document.getElementById('modalTitle').textContent = titulo;
    document.getElementById('modalMessage').textContent = mensaje;
    document.getElementById('modalForm').action = urlAccion;
    document.getElementById('confirmationModal').style.display = 'block';
}

function modelarInfoTurno(turnoDetalles) {
    const turnoInfo = document.createElement('div');
    
    const fechaInfo = document.createElement('p');
    fechaInfo.textContent = `Fecha: ${turnoDetalles.fecha_hora.split(' ')[0]}`; // Extraer solo la fecha
    turnoInfo.appendChild(fechaInfo);

    const horaInfo = document.createElement('p');
    horaInfo.textContent = `Hora: ${turnoDetalles.fecha_hora.split(' ')[1]}`; // Extraer solo la hora
    turnoInfo.appendChild(horaInfo);

    const especialidadInfo = document.createElement('p');
    especialidadInfo.textContent = `Especialidad: ${turnoDetalles.medico.especialidad}`; // Usar el atributo de médico
    turnoInfo.appendChild(especialidadInfo);

    const medicoInfo = document.createElement('p');
    medicoInfo.textContent = `Médico: ${turnoDetalles.medico.nombre} ${turnoDetalles.medico.apellido}`; // Usar los atributos de médico
    turnoInfo.appendChild(medicoInfo);

    return turnoInfo; // Devuelve el contenedor con la info del turno
}

function openPacienteModal(turno, pacientes) {
    const modalContent = document.getElementById('modalContent');
    modalContent.innerHTML = ''; // Limpia contenido previo

    // Mostrar información del turno
    const turnoInfo = modelarInfoTurno(turno);
    modalContent.appendChild(turnoInfo);

    // Limpiar el selector de pacientes
    const pacienteSelect = document.getElementById('pacienteSelect');
    pacienteSelect.innerHTML = '<option value="" disabled selected>Seleccione un paciente</option>'; // Opción por defecto

    // Llenar el selector de pacientes
    pacientes.forEach(paciente => {
        const option = document.createElement('option');
        option.value = paciente.id;
        option.textContent = `${paciente.nombre} ${paciente.apellido}`;
        pacienteSelect.appendChild(option);
    });

    // Asignar el ID del turno
    document.getElementById('turnoId').value = turno.id;

    // Mostrar el modal
    document.getElementById('pacienteModal').style.display = 'block';
}



// Función para cerrar cualquier modal
function closeModal() {
    document.getElementById('confirmationModal').style.display = 'none';
    document.getElementById('pacienteModal').style.display = 'none';
}
