from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand
from turnos.models import Medico, Paciente, Especialidad
from turnos.utils import create_user
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Genera datos de prueba para médicos, especialidades y pacientes'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.especialidades = []
        self.fake = Faker(['es_AR'])

    def handle(self, *args, **kwargs):
        self.create_groups()
        self.create_users()
        self.create_especialidades()
        self.create_medicos()
        self.create_pacientes(10)
        self.stdout.write(self.style.SUCCESS('Datos de prueba generados exitosamente.'))

    def create_groups(self):
        # Creamos los grupos para roles
        jefatura_recepcion_group, _ = Group.objects.get_or_create(name='Jefatura Recepcion')
        recepcionistas_group, _ = Group.objects.get_or_create(name='Recepcionistas')
        medicos_group, _ = Group.objects.get_or_create(name='Medicos')

        # Definimos los permisos
        jefatura_recepcion_permissions = [
            'view_session',
            'view_medico',
            'add_medico',
            'change_medico',
            'delete_medico',
            'view_paciente',
            'add_paciente',
            'change_paciente',
            'delete_paciente',          
            'view_especialidad',
            'add_especialidad',
            'change_especialidad',
            'delete_especialidad',
            'view_turno',
            'change_turno',
        ]
        recepcionista_permissions = [
            'view_session',
            'view_medico',
            'add_paciente',
            'change_paciente',
            'delete_paciente',
            'view_paciente',
            'change_turno',
            'view_turno',
            'view_especialidad'
        ]
        medico_permissions = ['view_turno']

        # Asignamos permisos

        for permiso_codename in jefatura_recepcion_permissions:
            perm = Permission.objects.get(codename=permiso_codename)
            jefatura_recepcion_group.permissions.add(perm)

        for permiso_codename in recepcionista_permissions:
            perm = Permission.objects.get(codename=permiso_codename)
            recepcionistas_group.permissions.add(perm)

        for permiso_codename in medico_permissions:
            perm = Permission.objects.get(codename=permiso_codename)
            medicos_group.permissions.add(perm)

        self.stdout.write(self.style.SUCCESS('Grupos creados y permisos asignados exitosamente.'))

    def create_users(self):
        # Crear superusuario
        create_user('admin', 'admin', '', True, True, None)

        # Crear usuario jefe recepcion
        create_user('jefe-recepcion', 'jefe-recepcion', 'jefe-recepcion@seprice.com', True, False, 'Jefatura Recepcion')
   
        # Crear usuario recepcionista
        create_user('recepcion', 'recepcion', 'recepcion@seprice.com', True, False, 'Recepcionistas')

        # Los usuarios de médicos se crean cuando se crea el medico

        self.stdout.write(self.style.SUCCESS('Usuarios admin y recepcion creados exitosamente.'))

    def create_especialidades(self):
        especialidades = [
            {
                'nombre': 'kinesiologia',
                'duracion_turno': 25,
                'valor_turno': 10000
            },
            {
                'nombre': 'salud_mental',
                'duracion_turno': 30,
                'valor_turno': 12000
            },
            {
                'nombre': 'clinica',
                'duracion_turno': 15,
                'valor_turno': 8000
            },
            {
                'nombre': 'cardiologia',
                'duracion_turno': 15,
                'valor_turno': 10000
            }
        ]

        for especialidad in especialidades:
            _, created = Especialidad.objects.get_or_create(
                nombre=especialidad['nombre'], 
                defaults={
                    'duracion_turno': especialidad['duracion_turno'], 
                    'valor_turno': especialidad['valor_turno']
                }
            )
            if created:
                self.especialidades.append(Especialidad.objects.get(nombre=especialidad['nombre']))

            self.stdout.write(self.style.SUCCESS('Especialidades creadas.'))

    def create_medicos(self):
        for especialidad in self.especialidades:
            for i in range(3):
                Medico.objects.create(
                    nombre=self.fake.first_name(),
                    apellido=self.fake.last_name(),
                    dni=str(random.randint(3000000, 90000000)),
                    matricula=str(random.randint(10000, 99999)),
                    especialidad=especialidad,
                    telefono=f'123456789{i}',
                    email=f'medico{i}@example.com',
                    domicilio_calle='Calle Falsa',
                    domicilio_numero=str(random.randint(1, 100)),
                    codigo_postal=str(random.randint(1000, 9999)),
                    provincia='Provincia',
                    pais='Argentina'
                )
        self.stdout.write(self.style.SUCCESS(f'Medicos creados exitosamente, con sus correspondientes turnos y usuarios'))

    def create_pacientes(self, cantidad):
        for i in range(cantidad):
            dni = str(random.randint(1000000, 99999999))
            Paciente.objects.create(
                nombre=self.fake.first_name(),
                apellido=self.fake.last_name(),
                dni=dni,
                telefono=f'123456789{i}',
                email=f'paciente{i}@example.com',
                domicilio_calle='Calle Falsa',
                domicilio_numero=str(random.randint(1, 100)),
                codigo_postal=str(random.randint(1000, 9999)),
                provincia='Provincia',
                pais='Argentina'
            )
        self.stdout.write(self.style.SUCCESS(f'Pacientes creados exitosamente'))


