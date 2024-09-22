# turnos/models/especialidad.py

from django.db import models
from django.core.exceptions import ValidationError

class Especialidad(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    duracion_turno = models.IntegerField()
    valor_turno = models.FloatField()

    class Meta:
    # esto es para prevenir en el admin que ponga mal el plural
        verbose_name = "Especialidad"
        verbose_name_plural = "Especialidades"

    def __str__(self):
        return self.nombre
       
    
    def delete(self, *args, **kwargs):
        # Validar que no haya médicos asociados a esta especialidad
        if self.pk and self.medico_set.exists():
            raise ValidationError("No se puede eliminar la especialidad porque está asociada a uno o más médicos.")
        super().delete(*args, **kwargs) 