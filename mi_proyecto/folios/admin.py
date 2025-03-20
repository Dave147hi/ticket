from django.contrib import admin
from .models import Folio, Comentario

@admin.register(Folio)
class FolioAdmin(admin.ModelAdmin):
    list_display = ('folio', 'asesor', 'fecha_apertura', 'estatus')
    search_fields = ('folio', 'asesor__username', 'contacto')
    list_filter = ('estatus', 'area', 'localidad')

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('folio', 'usuario', 'fecha', 'hora')
    search_fields = ('folio__folio', 'usuario__username')