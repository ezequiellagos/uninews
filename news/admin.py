from django.contrib import admin
from .models import Noticia, Universidad, Region

# Register your models here.
class UniversidadAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated', 'id_universidad')
    list_display = ('id_universidad', 'nombre', 'alias', 'region')
    list_filter = ('region',)

class NoticiaAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated', 'id_noticia', 'contador_visitas')
    list_display = ('titulo', 'fecha', 'get_alias', 'categoria', 'contador_visitas')
    ordering = ('-fecha', 'id_universidad', 'categoria', 'contador_visitas')
    search_fields = ('titulo', 'categoria', 'fecha', 'id_noticia')
    date_hierarchy = 'fecha'
    list_filter = ('id_universidad__alias', 'categoria', 'id_universidad__region')

    def get_alias(self, obj):
        return obj.id_universidad.alias
    get_alias.short_description = 'Alias'
    get_alias.admin_order_field = 'id_universidad__alias'

class RegionAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated', 'id_region')
    list_display = ('id_region', 'nombre', 'slug', 'numero_region', 'letra_region')
    prepopulated_fields = {"slug": ("nombre",)}

admin.site.register(Noticia, NoticiaAdmin)
admin.site.register(Universidad, UniversidadAdmin)
admin.site.register(Region, RegionAdmin)