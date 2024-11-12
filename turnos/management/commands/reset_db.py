# turnos/management/commands/reset_database.py

import os
import glob
from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = "Reset the database by deleting migrations, database file, and re-running migrations with test data."

    def handle(self, *args, **kwargs):
        # Borrar todas las migraciones (salvo __init__.py)
        migrations_dir = os.path.join('turnos', 'migrations')
        if os.path.isdir(migrations_dir):
            for migration_file in glob.glob(os.path.join(migrations_dir, '*.py')):
                if not migration_file.endswith('__init__.py'):
                    os.remove(migration_file)
                    self.stdout.write(self.style.SUCCESS(f'Eliminado: {migration_file}'))

        # Borrar el archivo db.sqlite3
        db_file = 'db.sqlite3'
        if os.path.exists(db_file):
            os.remove(db_file)
            self.stdout.write(self.style.SUCCESS(f'Eliminado: {db_file}'))
        
        # Correr las migraciones y generar datos de prueba
        call_command('makemigrations')
        call_command('migrate')
        call_command('generar_datos_prueba')
        self.stdout.write(self.style.SUCCESS('Base de datos reseteada y datos de prueba generados.'))
