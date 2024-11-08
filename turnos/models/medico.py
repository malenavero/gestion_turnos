# turnos/models/medico.py
from datetime import timedelta
from django.db import models
from django.forms import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User

from turnos.models.especialidad import Especialidad
from turnos.utils import create_user

class Medico(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
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

    def delete(self, *args, **kwargs):
        # Verificar si el médico tiene turnos que no estén en estado 'disponible'
        from turnos.models.turno import Turno
        if Turno.objects.filter(medico=self).exclude(estado='disponible').exists():
            raise ValidationError("No se puede eliminar el médico porque tiene turnos asociados.")

        # Si todos los turnos están disponibles, eliminar los turnos y luego el médico
        Turno.objects.filter(medico=self).delete()

        super().delete(*args, **kwargs)

        
    def save(self, *args, **kwargs):
        is_new = self.pk is None  # Comprueba si el médico es nuevo
        super().save(*args, **kwargs)  
        if is_new:
            print(f"Especialidad del médico: {self.especialidad} {self.especialidad.pk}")

            # Creamos turnos para el próximo mes
            self.generar_turnos(self)

            # Generamos un user en el grupo medicos con su primer nombre y apellido
            first_name = self.nombre.split()[0].lower()
            last_name = self.apellido.split()[0].lower()

            username = f"{first_name}.{last_name}"
            email = f"{username}@seprice.com"
            password = 'medico'

        user = create_user(username, password, True, False, 'Medicos', first_name, last_name)
        self.user = user
        self.email = email  # Asignar el email creado al campo de correo del médico
        self.save(update_fields=['user', 'email'])

        self.save(update_fields=['user'])

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
        inicio_turno = 8
        fin_turno = 10

        start_date = timezone.localtime().replace(hour=inicio_turno, minute=0, second=0, microsecond=0)
        end_date = timezone.localtime().replace(hour=fin_turno, minute=0, second=0, microsecond=0)
        next_month = timezone.localtime() + timedelta(days=30)
        
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
                    # Avanzar la cantidad de minutos que dura el turno
                    current_date += timedelta(minutes=medico.especialidad.duracion_turno)
                
                # Mover al siguiente dia siempre y cuando se encuentre en el mes
                current_date = Medico.getNextDay(current_date)
                


    def calcular_honorarios(self, mes, año):
        from turnos.models.turno import Turno
        from django.db.models import Q  

        # Definir el filtro base
        base_query = Q(medico_id=self.id, fecha_hora__month=mes, fecha_hora__year=año)

        turnos_atendidos = Turno.objects.filter(base_query, estado='atendido')
        turnos_ausentes_acreditados = Turno.objects.filter(base_query, estado='ausente_acreditado')

        total_honorarios_atendidos = sum(self.especialidad.valor_turno for turno in turnos_atendidos)
        total_honorarios_ausentes = sum(self.especialidad.valor_turno for turno in turnos_ausentes_acreditados)

        total_honorarios = total_honorarios_atendidos + total_honorarios_ausentes

        return total_honorarios, turnos_atendidos.count(), turnos_ausentes_acreditados.count()
