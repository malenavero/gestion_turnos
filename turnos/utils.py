 # turnos/utils.py

from django.utils import timezone
from django.contrib.auth.models import Group, User
from django.core.exceptions import ObjectDoesNotExist

def create_user(username, password, email, is_staff, is_superuser, group_name):
    # Primero verificamos si el usuario ya existe
    user = User.objects.filter(username=username).first()
    
    if user:
        print(f"El usuario '{username}' ya existe.")
        return

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
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
         # Si la fecha está vacía, filtrar desde hoy en adelante
        turnos = turnos.filter(fecha_hora__gte=timezone.now())
    return turnos

