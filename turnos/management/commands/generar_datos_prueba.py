from django.core.management.base import BaseCommand
from turnos.models import Medico, Paciente, Especialidad
import random


class Command(BaseCommand):
    help = 'Genera datos de prueba para médicos, especialidades y pacientes'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.especialidades = []

    def handle(self, *args, **kwargs):
        self.create_especialidades()
        self.create_medicos(10)
        self.create_pacientes(10)
        self.stdout.write(self.style.SUCCESS('Datos de prueba generados exitosamente.'))

    def create_especialidades(self):
        especialidades = ['Cardiología', 'Dermatología', 'Ginecología', 'Pediatría', 'Neurología']
        for especialidad in especialidades:
            _, created = Especialidad.objects.get_or_create(nombre=especialidad)
            if created:
                self.especialidades.append(Especialidad.objects.get(nombre=especialidad))
        self.stdout.write(self.style.SUCCESS('Especialidades creadas.'))


    def create_medicos(self, cantidad):
        for i in range(cantidad):
            dni = str(random.randint(3000000, 90000000))
            matricula = str(random.randint(10000, 99999))
            especialidad = random.choice(self.especialidades)
            medico = Medico.objects.create(
                nombre=f'Medico{i}',
                apellido=f'Apellido{i}',
                dni=dni,
                matricula=matricula,
                especialidad=especialidad,
                telefono=f'123456789{i}',
                email=f'medico{i}@example.com',
                domicilio_calle='Calle Falsa',
                domicilio_numero=str(random.randint(1, 100)),
                codigo_postal=str(random.randint(1000, 9999)),
                provincia='Provincia',
                pais='Argentina'
            )
            self.stdout.write(f'Médico creado: {medico}')
            Medico.generar_turnos(medico)

    def create_pacientes(self, cantidad):
        for i in range(cantidad):
            dni = str(random.randint(1000000, 99999999))
            paciente = Paciente.objects.create(
                nombre=f'Paciente{i}',
                apellido=f'Apellido{i}',
                dni=dni,
                telefono=f'123456789{i}',
                email=f'paciente{i}@example.com',
                domicilio_calle='Calle Falsa',
                domicilio_numero=str(random.randint(1, 100)),
                codigo_postal=str(random.randint(1000, 9999)),
                provincia='Provincia',
                pais='Argentina'
            )
            self.stdout.write(f'Paciente creado: {paciente}')
