from django.contrib import admin
from .models import Noticia, Universidad

# Register your models here.
class UniversidadAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated', 'id_universidad')

class NoticiaAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated', 'id_noticia', 'contador_visitas')

admin.site.register(Noticia, NoticiaAdmin)
admin.site.register(Universidad, UniversidadAdmin)