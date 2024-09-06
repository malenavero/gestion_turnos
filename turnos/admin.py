# turnos/admin.py
from datetime import datetime, timedelta
from django.contrib import admin

# Register your models here.
# admin.py

from django.contrib import admin

from turnos.models.especialidad import Especialidad
from .models import Paciente, Medico, Turno

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'dni', 'nro_historia_clinica')
    search_fields = ('nombre', 'apellido', 'dni')

@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'dni', 'especialidad', 'matricula')
    search_fields = ('nombre', 'apellido', 'dni', 'especialidad')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:  # Solo cuando se crea un nuevo médico
            Medico.generar_turnos(obj)


@admin.register(Turno)
class TurnoAdmin(admin.ModelAdmin):
    list_display = ('medico', 'fecha_hora', 'estado', 'paciente')
    list_filter = ('estado', 'medico__especialidad', 'medico')
    search_fields = ('medico__nombre', 'paciente__apellido')

    def duracion_display(self, obj):
        return f"{obj.duracion} minutos"
    duracion_display.short_description = 'Duración'

    class Media:
        js = ('admin/js/turno_admin.js',)
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Si estamos editando un turno existente
            return self.readonly_fields + ('duracion_display',)
        return self.readonly_fields

    
    def get_list_filter(self, request):
        # Add a filter for the date range
        filters = super().get_list_filter(request)
        filters = list(filters) + [DateRangeFilter]
        return filters

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # You can filter the queryset here if needed
        return qs
    
    def save_model(self, request, obj, form, change):
        if obj.paciente:
            obj.estado = 'ocupado'
        else:
            obj.estado = 'disponible'
        super().save_model(request, obj, form, change)


@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'duracion_turno')
    search_fields = ('nombre',)


# Custom filter for date range
from django.utils.translation import gettext_lazy as _
from django.contrib.admin import SimpleListFilter

class DateRangeFilter(SimpleListFilter):
    title = _('Date range')
    parameter_name = 'date_range'

    def lookups(self, request, model_admin):
        return [
            ('week', _('This week')),
            ('month', _('This month')),
        ]

    def queryset(self, request, queryset):
        value = self.value()
        now = datetime.now()
        if value == 'week':
            start_date = now - timedelta(days=now.weekday())
            end_date = start_date + timedelta(days=7)
            return queryset.filter(fecha_hora__range=[start_date, end_date])
        elif value == 'month':
            start_date = now.replace(day=1)
            end_date = (start_date + timedelta(days=31)).replace(day=1)
            return queryset.filter(fecha_hora__range=[start_date, end_date])
        return queryset