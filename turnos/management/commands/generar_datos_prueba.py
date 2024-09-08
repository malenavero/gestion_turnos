from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.management.base import BaseCommand
from turnos.models import Medico, Paciente, Especialidad
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Genera datos de prueba para médicos, especialidades y pacientes'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.especialidades = []

    def handle(self, *args, **kwargs):
        self.create_groups()
        self.create_users()
        self.create_especialidades()
        self.create_medicos()
        self.create_pacientes(10)
        self.stdout.write(self.style.SUCCESS('Datos de prueba generados exitosamente.'))

    def create_groups(self):
        # Creamos los grupos para roles
        recepcionistas_group, _ = Group.objects.get_or_create(name='Recepcionistas')
        medicos_group, _ = Group.objects.get_or_create(name='Medicos')

        # Definimos los permisos
        recepcionista_permissions = [
            'view_user',
            'view_session',
            'add_medico',
            'change_medico',
            'delete_medico',
            'view_medico',
            'add_paciente',
            'change_paciente',
            'delete_paciente',
            'view_paciente',
            'change_turno',
            'view_turno',
            'add_especialidad',
            'change_especialidad',
            'delete_especialidad',
            'view_especialidad'
        ]
        medico_permissions = ['view_turno']

        # Asignamos permisos
        for permiso_codename in recepcionista_permissions:
            perm = Permission.objects.get(codename=permiso_codename)
            recepcionistas_group.permissions.add(perm)

        for permiso_codename in medico_permissions:
            perm = Permission.objects.get(codename=permiso_codename)
            medicos_group.permissions.add(perm)

        self.stdout.write(self.style.SUCCESS('Grupos creados y permisos asignados exitosamente.'))

    def create_users(self):
        # Crear superusuario
        User.objects.get_or_create(username='admin', defaults={
            'is_superuser': True,
            'is_staff': True,
            'email': '',
            'password': 'admin'
        })

        # Crear usuario recepcionista
        recepcionista_user, created = User.objects.get_or_create(username='recepcion', defaults={
            'is_superuser': False,
            'is_staff': True,
            'email': 'recepcion@seprice.com',
            'password': 'recepcion'
            
        })
        if created:
            recepcionista_user.groups.add(Group.objects.get(name='Recepcionistas'))

        # Los usuarios de médicos se crean cuando se crea el medico

        self.stdout.write(self.style.SUCCESS('Usuarios creados exitosamente.'))

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
        print(f'PRINTTT{self.especialidades}')
        for especialidad in self.especialidades:
            for i in range(3):
                medico = Medico.objects.create(
                    nombre=f'Medico{i}',
                    apellido=especialidad.nombre,
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


