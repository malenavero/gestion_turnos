# turnos/models/turno.py

from datetime import timedelta
from django.db import models
from django.forms import ValidationError
from django.utils import timezone

from turnos.models.medico import Medico
from turnos.models.paciente import Paciente

class Turno(models.Model):
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_hora = models.DateTimeField()
    duracion = models.DurationField(default=timedelta(minutes=15))
    
    ESTADO_CHOICES = [
        ('disponible', 'Disponible'),
        ('ocupado', 'Ocupado'),
        ('bloqueado', 'Bloqueado'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='disponible')
    
    def clean(self):
        super().clean()
        if Turno.objects.filter(medico=self.medico, fecha_hora=self.fecha_hora).exclude(id=self.id).exists():
            raise ValidationError('Ya existe un turno asignado para este médico en el mismo horario.')

    def save(self, *args, **kwargs):
       # fecha_hora consistente con zona horaria
        if timezone.is_naive(self.fecha_hora):
            self.fecha_hora = timezone.make_aware(self.fecha_hora, timezone.get_current_timezone())
        
        if self.duracion != timedelta(minutes=15):
            raise ValidationError('La duración del turno debe ser exactamente 15 minutos.')

        # limpia y valida
        self.full_clean()
        
        # actualiza estado turno
        if self.paciente:
            self.estado = 'ocupado'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Turno con {self.medico} el {self.fecha_hora} - {self.get_estado_display()}"
