
# turnos/models/historia_clinica.py
from django.db import models
from django.utils import timezone

from turnos.models import Paciente,Medico


class HistoriaClinica(models.Model):
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE, related_name='historia_clinica')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Historia Clínica de {self.paciente.nombre} {self.paciente.apellido}"

    class Meta:
        verbose_name = "Historia Clínica"
        verbose_name_plural = "Historias Clínicas"

class EntradaHistoria(models.Model):
    historia_clinica = models.ForeignKey(HistoriaClinica, on_delete=models.CASCADE, related_name='entradas')
    fecha = models.DateTimeField(auto_now_add=True)
    diagnostico = models.TextField()
    tratamiento = models.TextField()
    receta = models.TextField(blank=True, null=True)
    notas_adicionales = models.TextField(blank=True, null=True)
    medico = models.ForeignKey(Medico, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Entrada {self.fecha.strftime('%Y-%m-%d')} - {self.historia_clinica.paciente.nombre} {self.historia_clinica.paciente.apellido}"

    class Meta:
        verbose_name = "Entrada de Historia Clínica"
        verbose_name_plural = "Entradas de Historias Clínicas"
