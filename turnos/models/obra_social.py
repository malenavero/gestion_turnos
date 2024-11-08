# turnos/models/obra_social.py

from django.db import models

class ObraSocial(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    planes = models.JSONField(blank=True, default=list)

    class Meta:
    # esto es para prevenir en el admin que ponga mal el plural
        verbose_name = "Obra Social"
        verbose_name_plural = "Obras Sociales"

    def __str__(self):
        return self.nombre.capitalize()       
    
