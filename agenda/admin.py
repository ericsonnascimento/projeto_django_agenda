from django.contrib import admin
from agenda.models import Evento

class EventoAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'data_evento', 'data_criacao')

admin.site.register(Evento, EventoAdmin)
