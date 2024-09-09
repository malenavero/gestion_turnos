// turnos/static/admin/js/turno_admin.js
document.addEventListener('DOMContentLoaded', function() {
    const loadTurnosJs = window.location.pathname.includes('/admin/turnos/turno/') && window.location.pathname.includes('/change/');

    // Nos aseguramos que eso se ejecute solamente en la pantalla de editar turnos
    if (loadTurnosJs) {
        // Obtenemos los elementos del DOM
        const pacienteField = document.getElementById('id_paciente');
        const estadoField = document.getElementById('id_estado');

        // Seteamos los campos que correspondan en disabled
        function setInitialDisabled() {
            if(estadoField.value === 'ocupado') {
                disableField(estadoField, true);
            } else if (estadoField.value === 'bloqueado') {
                disableField(pacienteField, true);
            }
        }

        // Funcion para darle el estilo al field en caso de deshabilitarlo
        function disableField(field, disabled) {
            if (disabled) {
                field.setAttribute('disabled', true);
                field.style.cursor = 'not-allowed';  
                field.style.backgroundColor = '#d2d4d6';  // Fondo gris claro
                field.style.color = '#6c757d';  // Letra gris oscuro
            } else {
                field.removeAttribute('disabled'); 
                field.style.cursor = '';  
                field.style.backgroundColor = '';  // Fondo por defecto
                field.style.color = '';  // Letra por defecto
            }
        }

        // Función para actualizar el estado y ver si es solo lectura
        function updateEstadoField() {
            if (pacienteField.value) {
                estadoField.value = 'ocupado';
                disableField(estadoField, true);
            } else {
                estadoField.value = 'disponible';
                disableField(estadoField, false);
            }
        }

        // Función para actualizar el estado y ver si es solo lectura
        function updatePacienteField() {

            if (estadoField.value == 'bloqueado') {
                disableField(pacienteField, true);
            } else {
                disableField(pacienteField, false);
            }
        }

        // Agrega un listener para el campo paciente
        pacienteField.addEventListener('change', function() {
            updateEstadoField();
        });

        // Agrega un listener para el campo estado
        estadoField.addEventListener('change', function() {
            updatePacienteField();
        });

        // Inicializa el estado disabled cuando se carga la página
        setInitialDisabled();

        // Habilita los campos antes de enviar el formulario
        const form = document.getElementById('turno_form');
        if (form) {
            form.addEventListener('submit', function() {
                // Esto es necesario porque en js los campos select solo se pueden hacer read only con disabled,
                //  pero a su vez si etsan disabled no se mandan en el form, 
                //  por lo que los habilitamos para guardarlos 
                //  y despues al cargar la pag los volvemos a deshabilitar
                disableField(estadoField, false);
                disableField(pacienteField, false);
            });
        }
    }
});
