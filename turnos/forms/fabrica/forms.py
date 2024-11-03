from django import forms
from turnos.models import Especialidad, Paciente, Medico
from django import forms

class EspecialidadForm(forms.ModelForm):
    class Meta:
        model = Especialidad
        fields = ['nombre', 'duracion_turno', 'valor_turno']

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = fields = [
            'nombre',
            'apellido',
            'dni',
            'obra_social',
            'credencial',
            'telefono',
            'email',
            'domicilio_calle',
            'domicilio_numero',
            'codigo_postal',
            'provincia',
            'pais',
        ]

class MedicoForm(forms.ModelForm):
    especialidad = forms.ModelChoiceField(queryset=Especialidad.objects.all(), empty_label="Seleccione Especialidad")

    class Meta:
        model = Medico
        fields = [
            'nombre', 'apellido', 'dni', 'matricula', 'especialidad', 'telefono', 
            'email', 'domicilio_calle', 'domicilio_numero', 'codigo_postal', 
            'provincia', 'pais',
        ]

    def __init__(self, *args, disable_especialidad=False, **kwargs):
        super().__init__(*args, **kwargs)
        if disable_especialidad:
            self.fields['especialidad'].widget.attrs['readonly'] = 'readonly'
        self.fields['especialidad'].widget.attrs.update({'class': 'form-control'})
