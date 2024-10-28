//turnos/static/js/modals.js

// Función para abrir el Modal de Confirmación de eliminacion

let selectedTurnoId = null; // Variable global para almacenar el turno seleccionado
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

/*
***
* FUNCIONES RELACIONADAS A MODAL DE PAGO
***
*/
function openAcreditacionModal(turnoId, urlAccion) {
    const urlFinal = urlAccion.replace('0', turnoId);

    selectedTurnoId = turnoId;
    nextURL = urlFinal;
    document.getElementById('acreditacionModal').style.display = 'block';
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('fechaVencimiento').setAttribute('min', today);
}

function handleAcreditacionOption(option) {   
    switch (option) {
        case 'particular':
            console.log(`Gestionar pago: ${selectedTurnoId}`);
            document.getElementById('acreditacionParticularModalForm').action = nextURL;
            document.getElementById('acreditacionParticularModal').style.display = 'block';
            break;

        case 'obra-social':
            console.log(`Gestionar autorizacion: ${selectedTurnoId}`);
            document.getElementById('acreditacionObraSocialModalForm').action = nextURL;
            document.getElementById('acreditacionObraSocialModal').style.display = 'block';
            break;
    }
    
    // Cerrar el modal después de hacer clic en cualquier botón
    closeModal('acreditacionModal');
}

// Función para mostrar u ocultar campos según el método de pago seleccionado
function togglePaymentFields() {
    const paymentMethod = document.getElementById('paymentMethod').value;
    const tarjetaFields = document.getElementById('tarjetaFields');
    const cardTypeLabel = document.getElementById('cardTypeLabel');

    if (paymentMethod === 'tarjeta') {
        tarjetaFields.style.display = 'block';
        // Agregar el atributo required a los campos de tarjeta
        document.getElementById('nombreApellido').setAttribute('required', 'required');
        document.getElementById('nroTarjeta').setAttribute('required', 'required');
        document.getElementById('fechaVencimiento').setAttribute('required', 'required');
        document.getElementById('codSeguridad').setAttribute('required', 'required');
    } else {
        tarjetaFields.style.display = 'none';
        cardTypeLabel.style.display = 'none'; // Ocultar el tipo de tarjeta si no se usa tarjeta
        document.getElementById('cuotasContainer').style.display = 'none';
        
        // Remover el atributo required de los campos de tarjeta
        document.getElementById('nombreApellido').removeAttribute('required');
        document.getElementById('nroTarjeta').removeAttribute('required');
        document.getElementById('fechaVencimiento').removeAttribute('required');
        document.getElementById('codSeguridad').removeAttribute('required');
    }
}

// Funcion para detectar que tipo de tarjeta es y mostrar
function detectCardType() {
    const cardInput = document.getElementById('nroTarjeta');
    const cardTypeLabel = document.getElementById('cardTypeLabel');
    const cuotasContainer = document.getElementById('cuotasContainer');
    let cardNumber = cardInput.value.replace(/\D/g, ''); // Remove non-numeric characters

    // Regular expressions for different card types
    const VISA = /^4[0-9]{0,15}$/;
    const MASTERCARD = /^5[1-5][0-9]{0,14}$/;
    const AMEX = /^3[47][0-9]{0,13}$/;  // 15 digits for Amex, starting with 34 or 37
    const CABAL = /^(6042|6043|6044|6045|6046|5896)[0-9]{0,10}$/;
    const NARANJA = /^(589562|402917|402918|527571|527572|0377798|0377799)[0-9]*$/;

    // Reset label and visibility of the installment container
    cardTypeLabel.style.display = 'none';
    cuotasContainer.style.display = 'none';
    
    // Variables for card type and formatting
    let maxDigits = 16;
    let formatPattern = '#### #### #### ####';

    // Card type detection logic based on regex
    if (AMEX.test(cardNumber)) {
        cardTypeLabel.textContent = "AMEX";
        maxDigits = 15;
        formatPattern = '#### ###### #####';
        cardTypeLabel.style.display = 'block';
        cuotasContainer.style.display = 'none'; // Hide installments for Amex
    } else if (VISA.test(cardNumber)) {
        cardTypeLabel.textContent = "VISA";
        maxDigits = 16;
        formatPattern = '#### #### #### ####';
        cardTypeLabel.style.display = 'block';
        cuotasContainer.style.display = 'block';
    } else if (MASTERCARD.test(cardNumber)) {
        cardTypeLabel.textContent = "MASTERCARD";
        maxDigits = 16;
        formatPattern = '#### #### #### ####';
        cardTypeLabel.style.display = 'block';
        cuotasContainer.style.display = 'block';
    } else if (CABAL.test(cardNumber)) {
        cardTypeLabel.textContent = "CABAL";
        maxDigits = 16;
        formatPattern = '#### #### #### ####';
        cardTypeLabel.style.display = 'block';
        cuotasContainer.style.display = 'block';
    } else if (NARANJA.test(cardNumber)) {
        cardTypeLabel.textContent = "NARANJA";
        maxDigits = 16;
        formatPattern = '#### #### #### ####';
        cardTypeLabel.style.display = 'block';
        cuotasContainer.style.display = 'block';
    } else {
        cardTypeLabel.textContent = ""; // Clear if card type is not detected
    }

    // Apply color based on card detection
    if (cardTypeLabel.textContent) {
        cardInput.classList.remove('input-error');
        cardInput.classList.add('input-valid');
    } else {
        cardInput.classList.remove('input-valid');
        cardInput.classList.add('input-error');
    }


    // Limit input length based on digits only, without spaces
    cardNumber = cardNumber.substring(0, maxDigits);

    // Apply formatting as user types
    cardInput.value = formatCardNumber(cardNumber, formatPattern);
}

// Funcion para formatear el nro segun el tipo de tarjeta
function formatCardNumber(number, pattern) {
    let formatted = '';
    let index = 0;

    for (const char of pattern) {
        if (char === '#') {
            if (index < number.length) {
                formatted += number[index];
                index++;
            } else {
                break;
            }
        } else {
            formatted += char;
        }
    }

    return formatted;
}

 // Función para ocultar el código de seguridad con asteriscos
function maskSecurityCode() {
    const securityCodeInput = document.getElementById('codSeguridad');
    const value = securityCodeInput.value;
    
    // Reemplaza el valor por asteriscos
    securityCodeInput.value = '*'.repeat(value.length);
}

function showSuccessPaymentModal() {
    document.getElementById('successModal').style.display = 'block';
}


// Función para abrir el Modal de llamado al consultorio
function openConsultorioModal(turnoId) {
    selectedTurnoId = turnoId;
    document.getElementById('consultorioModal').style.display = 'block';
}

function handleLLamadoConsultorioOption(option, urlAccion) {
    if (!selectedTurnoId) {
        console.error("Error: Turno ID no asignado.");
        return;
    }
    // URL final con el turnoId y la acción
    let urlFinal = urlAccion.replace('0', selectedTurnoId);
    urlFinal = urlFinal.replace('accion', option);
    
    // Establece la acción del formulario y lo envía
    const form = document.getElementById('acreditacionObraSocialModalForm');
    form.action = urlFinal;
    form.submit();
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



/*
***
*EVENTOS
***
*/


