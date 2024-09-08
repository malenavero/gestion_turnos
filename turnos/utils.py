
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