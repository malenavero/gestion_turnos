//turnos/static/js/modals.js

// Función para abrir el Modal de Confirmación de eliminacion

let selectedTurno = null; // Variable global para almacenar el turno seleccionado
let nextURL = null;


function openConfirmacionModal(titulo, mensaje, urlAccion) {
    document.getElementById('modalTitle').textContent = titulo;
    document.getElementById('modalMessage').textContent = mensaje;
    document.getElementById('modalForm').action = urlAccion;
    document.getElementById('confirmationModal').style.display = 'block';
}

function modelarInfoTurno(turnoDetalles) {
    const turnoInfo = document.createElement('div');
    turnoInfo.classList.add('turno-info'); // Añade una clase para estilos

    // Crear un contenedor para los detalles
    const detailsContainer = document.createElement('div');
    detailsContainer.classList.add('details-container');

    // Crear elementos para los detalles
    const fechaInfo = document.createElement('p');
    fechaInfo.innerHTML = `<strong>Fecha:</strong> ${turnoDetalles.fecha_hora.split(' ')[0]}`;
    detailsContainer.appendChild(fechaInfo);

    const horaInfo = document.createElement('p');
    horaInfo.innerHTML = `<strong>Hora:</strong> ${turnoDetalles.fecha_hora.split(' ')[1]}`;
    detailsContainer.appendChild(horaInfo);

    const especialidadInfo = document.createElement('p');
    especialidadInfo.innerHTML = `<strong>Especialidad:</strong> ${turnoDetalles.medico.especialidad}`;
    detailsContainer.appendChild(especialidadInfo);

    const medicoInfo = document.createElement('p');
    medicoInfo.innerHTML = `<strong>Médico:</strong> ${turnoDetalles.medico.nombre} ${turnoDetalles.medico.apellido}`;
    detailsContainer.appendChild(medicoInfo);

    turnoInfo.appendChild(detailsContainer);
    
    return turnoInfo; 
}


function openPacienteModal(turnoData, pacientes, urlAccion) {
    const urlFinal = urlAccion.replace('0', turnoData.id);

    const modalContent = document.getElementById('modalContent');
    modalContent.innerHTML = ''; // Limpia contenido previo

    // Mostrar información del turno
    const turnoInfo = modelarInfoTurno(turnoData);
    modalContent.appendChild(turnoInfo);

    // Limpiar el selector de pacientes
    const pacienteSelect = document.getElementById('pacienteSelect');
    pacienteSelect.innerHTML = '<option value="" disabled selected>Seleccione un paciente</option>'; 

    // Llenar el selector de pacientes
    pacientes.forEach(paciente => {
        const option = document.createElement('option');
        option.value = paciente.id;
        option.textContent = `${paciente.nombre} ${paciente.apellido}`;
        pacienteSelect.appendChild(option);
    });

    // Mostrar el modal
    document.getElementById('pacienteModalForm').action = urlFinal;
    document.getElementById('pacienteModal').style.display = 'block';

}

// Función para abrir el Modal de Confirmación de Cancelar Turno
function openCancelTurnoModal(turnoId, urlAccion) {
    const urlFinal = urlAccion.replace('0', turnoId);
    document.getElementById('cancelModalForm').action = urlFinal;
    document.getElementById('cancelTurnoModal').style.display = 'block';
}

// Función para abrir el Modal de Bloqueo/Desbloqueo de Turno
function openBlockTurnoModal(turnoId, urlAccion, esBloqueado) {
    const urlFinal = urlAccion.replace('0', turnoId);
    const modalTitle = document.getElementById('blockModalTitle');
    const modalButton = document.getElementById('blockModalButton');
    
    // Ajustar título y botón según el estado del turno
    if (esBloqueado) {
        modalTitle.textContent = 'Desbloquear Turno';
        modalButton.textContent = 'Desbloquear';
        modalButton.classList.remove('bloquear-btn');
        modalButton.classList.add('desbloquear-btn');
    } else {
        modalTitle.textContent = 'Bloquear Turno';
        modalButton.textContent = 'Bloquear';
        modalButton.classList.remove('desbloquear-btn');
        modalButton.classList.add('bloquear-btn');
    }
    
    document.getElementById('blockModalForm').action = urlFinal;
    document.getElementById('blockTurnoModal').style.display = 'block';
}

// Función para abrir el Modal de acreditación
function openAcreditacionModal(turnoId, urlAccion) {
    const urlFinal = urlAccion.replace('0', turnoId);

    selectedTurno = turnoId;
    nextURL = urlFinal;
    document.getElementById('acreditacionModal').style.display = 'block';
}
function handleAcreditacionOption(option) {   
    switch (option) {
        case 'particular':
            console.log(`Gestionar pago: ${selectedTurno}`);
            document.getElementById('acreditacionParticularModalForm').action = nextURL;
            document.getElementById('acreditacionParticularModal').style.display = 'block';
            break;

        case 'obra-social':
            console.log(`Gestionar autorizacion: ${selectedTurno}`);
            document.getElementById('acreditacionObraSocialModalForm').action = nextURL;
            document.getElementById('acreditacionObraSocialModal').style.display = 'block';
            break;
    }
    
    // Cerrar el modal después de hacer clic en cualquier botón
    closeModal('acreditacionModal');
}

// Función para abrir el Modal de llamado al consultorio
function openConsultorioModal(turnoId) {
    document.getElementById('consultorioTurnoId').textContent = `ID del Turno: ${turnoId}`;
    document.getElementById('consultorioModal').style.display = 'block';
}

function handleLLamadoConsultorioOption(option) {
    const turnoId = document.getElementById('consultorioTurnoId').textContent.split(': ')[1];
    
    // Aquí puedes manejar cada opción como desees
    switch (option) {
        case 'llamar':
            console.log(`Llamar nuevamente el turno ID: ${turnoId}`);
            break;
        case 'ausente':
            console.log(`Marcar como ausente el turno ID: ${turnoId}`);
            break;
        case 'atender':
            console.log(`Comenzar a atender el turno ID: ${turnoId}`);
            break;
    }
    
    // Cerrar el modal después de hacer clic en cualquier botón
    closeModal('consultorioModal');
}



// Función para cerrar cualquier modal
// function closeModal() {
//     document.getElementById('confirmationModal').style.display = 'none';
//     document.getElementById('pacienteModal').style.display = 'none';
//     document.getElementById('cancelTurnoModal').style.display = 'none';
//     document.getElementById('blockTurnoModal').style.display = 'none';
//     document.getElementById('consultorioModal').style.display = 'none';
//     document.getElementById('acreditacionModal').style.display = 'none'; 

// }
function closeModal(modalId) {
    if(modalId){
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.style.display = 'none';
        }
    } else {
        closeAllModals()
    }
    
}
function closeAllModals() {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        modal.style.display = 'none';
    });
}
