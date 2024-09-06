from datetime import datetime, timedelta

from django.db import models

from turnos.models.especialidad import Especialidad

class Medico(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=8, unique=True)
    matricula = models.CharField(max_length=50, unique=True)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.SET_NULL, null=True)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()

    domicilio_calle = models.CharField(max_length=100, null=True, blank=True)
    domicilio_numero = models.CharField(max_length=10, null=True, blank=True)
    codigo_postal = models.CharField(max_length=10, null=True, blank=True)
    provincia = models.CharField(max_length=50, null=True, blank=True)
    pais = models.CharField(max_length=50, null=True, blank=True)
    
       
    def __str__(self):
        return f"Dr/a. {self.apellido}, {self.nombre} - {self.especialidad}"
    
    @staticmethod
    def getNextDay(current_date):
        next_day = current_date + timedelta(days=1)
        current_date = next_day.replace(hour=8, minute=0, second=0, microsecond=0)
        
        # Mover al siguiente mes si me paso
        if next_day.month != current_date.month:
            current_date = current_date.replace(day=1)
        return current_date
    
    @classmethod
    def generar_turnos(cls, medico=None):
        from turnos.models.turno import Turno

        start_date = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
        end_date = datetime.now().replace(hour=17, minute=0, second=0, microsecond=0)
        next_month = datetime.now() + timedelta(days=30)
        
        if medico:
            medicos = [medico]
        else:
            medicos = cls.objects.all()

        for medico in medicos:
            current_date = start_date
            while current_date < next_month:
                while current_date.time() <= end_date.time():
                    Turno.objects.get_or_create(
                        medico=medico,
                        fecha_hora=current_date,
                        defaults={'estado': 'disponible'}
                    )
                    current_date += timedelta(minutes=15)
                
                # Mover al siguiente dia siempre y cuando se encuentre en el mes

                current_date = Medico.getNextDay(current_date)
                

