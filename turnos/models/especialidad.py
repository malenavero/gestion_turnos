from django.db import models

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
