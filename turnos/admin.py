# turnos/admin.py
from datetime import timedelta
from django.utils import timezone
from django.contrib import admin
from .models import Paciente, Medico, Turno, Especialidad, HistoriaClinica, EntradaHistoria, ObraSocial


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'dni')
    search_fields = ('nombre', 'apellido', 'dni')

@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'dni', 'especialidad', 'matricula')
    search_fields = ('nombre', 'apellido', 'dni', 'especialidad')

@admin.register(Turno)
class TurnoAdmin(admin.ModelAdmin):
    list_display = ('medico', 'fecha_hora', 'estado', 'paciente')
    list_filter = ('estado', 'medico__especialidad', 'medico')
    search_fields = ('medico__nombre', 'paciente__apellido', 'paciente__nombre')

    def duracion_display(self, obj):
        return f"{obj.medico.especialidad.duracion_turno} minutos"
    duracion_display.short_description = 'Duración'

    class Media:
        js = ('admin/js/turno_admin.js',) 
        
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Si estamos editando un turno existente
            return self.readonly_fields + ('duracion_display', 'medico', 'fecha_hora')
        return self.readonly_fields
    
    def get_list_filter(self, request):
        # Agregamos un filtro para los rangos de fechas
        filters = super().get_list_filter(request)
        filters = list(filters) + [DateRangeFilter]
        return filters

    def get_queryset(self, request):
        # Permitir buscar turnos por fecha
        qs = super().get_queryset(request)
        return qs
    

@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'duracion_turno')
    search_fields = ('nombre',)

admin.site.register(HistoriaClinica)

@admin.register(ObraSocial)
class ObraSocialdAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'planes')
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
        now = timezone.now() 
        if value == 'week':
            start_date = now - timedelta(days=now.weekday())
            end_date = start_date + timedelta(days=7)
            return queryset.filter(fecha_hora__range=[start_date, end_date])
        elif value == 'month':
            start_date = now.replace(day=1)
            end_date = (start_date + timedelta(days=31)).replace(day=1)
            return queryset.filter(fecha_hora__range=[start_date, end_date])
        return queryset