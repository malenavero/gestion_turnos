# Generated by Django 4.2.15 on 2024-08-24 01:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('turnos', '0005_especialidad_alter_medico_dni_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='especialidad',
            options={'verbose_name': 'Especialidad', 'verbose_name_plural': 'Especialidades'},
        ),
    ]
