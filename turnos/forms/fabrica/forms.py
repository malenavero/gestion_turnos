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
    class Meta:
        model = Medico
        fields = [
            'nombre',
            'apellido',
            'dni',
            'matricula',
            'especialidad',
            'telefono',
            'email',
            'domicilio_calle',
            'domicilio_numero',
            'codigo_postal',
            'provincia',
            'pais',
        ]
    
    especialidad = forms.ModelChoiceField(queryset=Especialidad.objects.all(), empty_label="Seleccione Especialidad")


