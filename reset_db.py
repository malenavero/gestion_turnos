import os
import glob
import django
from django.core.management import call_command

# Configura el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_turnos.settings')  
django.setup()

def reset_database():
    # Borrar todas las migraciones (salvo __init__.py)
    migrations_dir = os.path.join('turnos', 'migrations')
    if os.path.isdir(migrations_dir):
        for migration_file in glob.glob(os.path.join(migrations_dir, '*.py')):
            if not migration_file.endswith('__init__.py'):
                os.remove(migration_file)
                print(f'Eliminado: {migration_file}')

    # Borrar el archivo db.sqlite3
    db_file = 'db.sqlite3'
    if os.path.exists(db_file):
        os.remove(db_file)
        print(f'Eliminado: {db_file}')
    
    # Correr las migraciones y generar datos de prueba
    call_command('makemigrations')
    call_command('migrate')
    call_command('generar_datos_prueba')  # Asegúrate de que este comando exista
    print('Base de datos reseteada y datos de prueba generados.')

if __name__ == '__main__':
    reset_database()
