from django.db import models
from django.forms import ValidationError

class Paciente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=8, unique=True)
    obra_social = models.CharField(max_length=100, null=True, blank=True)
    credencial = models.CharField(max_length=100, null=True, blank=True)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    
    nro_historia_clinica = models.PositiveIntegerField(unique=True, blank=True, null=True, editable=False)
    
    domicilio_calle = models.CharField(max_length=100, null=True, blank=True)
    domicilio_numero = models.CharField(max_length=10, null=True, blank=True)
    codigo_postal = models.CharField(max_length=10, null=True, blank=True)
    provincia = models.CharField(max_length=50, null=True, blank=True)
    pais = models.CharField(max_length=50, null=True, blank=True)
    
    def delete(self, *args, **kwargs):
        from turnos.models.turno import Turno
        # Verificar si el paciente tiene turnos asociados
        if Turno.objects.filter(paciente=self).exists():
            raise ValidationError("No se puede eliminar el paciente porque tiene turnos asociados.")
        
        super().delete(*args, **kwargs)


    def save(self, *args, **kwargs):
        if not self.nro_historia_clinica:
            # Si no tiene se busca el último y se incrementa de a uno
            last_patient = Paciente.objects.all().order_by('-nro_historia_clinica').first()
            if last_patient:
                self.nro_historia_clinica = last_patient.nro_historia_clinica + 1
            else:
                self.nro_historia_clinica = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.apellido}, {self.nombre} - {self.nro_historia_clinica}"
