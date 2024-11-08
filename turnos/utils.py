 # turnos/utils.py

from django.utils import timezone
from datetime import datetime, time
from django.contrib.auth.models import Group, User
from django.core.exceptions import ObjectDoesNotExist

from turnos.models.paciente import Paciente
from turnos.models.obra_social import ObraSocial


def create_user(first_name, last_name, password, is_staff, is_superuser, group_name):
    # Primero verificamos si el usuario ya existe
    nombre = first_name.split()[0].lower()
    apellido = last_name.split()[0].lower()
    username = f"{nombre}.{apellido}"
    user = User.objects.filter(username=username).first()
    
    if user:
        print(f"El usuario '{username}' ya existe.")
        return

    # Generamos el email a partir del nombre y apellido
    email = f"{nombre}.{apellido}@seprice.com"

    # Creamos el usuario
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=first_name,  
        last_name=last_name  
    )
    
    user.is_staff = is_staff
    user.is_superuser = is_superuser
    user.save()
    
    if group_name:
        try:
            group = Group.objects.get(name=group_name)
            user.groups.add(group)
        except ObjectDoesNotExist:
            print(f"El grupo '{group_name}' no existe.")
    
    print(f"Usuario creado: {username}")
    return user


def filtrar_turnos(turnos, query):

    if 'especialidad_id' in query and query['especialidad_id']:
        turnos = turnos.filter(medico__especialidad__id=query['especialidad_id'])
    if 'medico_id' in query and query['medico_id']:
        turnos = turnos.filter(medico__id=query['medico_id'])
    if 'paciente_id' in query and query['paciente_id']:
        turnos = turnos.filter(paciente__id=query['paciente_id'])
    if 'fecha' in query and query['fecha']:
        turnos = turnos.filter(fecha_hora__date=query['fecha'])
    else:
        # Filtrar desde hoy a las 8 AM
        hoy = timezone.localtime().date()
        fecha_inicio = timezone.make_aware(datetime.combine(hoy, time(8, 0)))  # 8 AM de hoy
        turnos = turnos.filter(fecha_hora__gte=fecha_inicio)

    return turnos

def get_month_name(month_number):
    months = [
        '',
        'Enero',
        'Febrero',
        'Marzo',
        'Abril',
        'Mayo',
        'Junio',
        'Julio',
        'Agosto',
        'Septiembre',
        'Octubre',
        'Noviembre',
        'Diciembre',
    ]
    return months[month_number]

def gestionar_cobro():
    print("TURNO COBRADO")

def gestionar_autorizacion(data_autorizacion):
    paciente_id = data_autorizacion['paciente_id']
    request = data_autorizacion['request']


    paciente = Paciente.objects.get(id=paciente_id)
    
    if request.method == 'POST':
        obra_social_id = request.POST.get('obra_social')
        paciente.obra_social = ObraSocial.objects.get(id=obra_social_id)
        paciente.credencial = request.POST.get('nro_credencial')
        paciente.plan = request.POST.get('plan')
        paciente.save() 