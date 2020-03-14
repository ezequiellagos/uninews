from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Noticia(models.Model):
    id_noticia = models.IntegerField(primary_key=True)
    titulo = models.CharField(max_length=200)
    titulo_busqueda = models.CharField(max_length=200, default=None)
    bajada = models.TextField()
    bajada_busqueda = models.TextField(default=None)
    fecha = models.DateField(blank=True, null=True)
    link_noticia = models.CharField(max_length=200)
    link_recurso = models.CharField(max_length=200)
    id_universidad = models.ForeignKey('Universidad', default=None, on_delete=models.PROTECT)
    categoria = models.CharField(max_length=100)
    contador_visitas = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    class Meta:
        verbose_name = "noticia"
        verbose_name_plural = "noticias"
        ordering = ["-fecha"]
    
    def __str__(self):
        return self.titulo

class Universidad(models.Model):
    id_universidad = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    alias = models.CharField(max_length=10)
    region = models.ForeignKey('Region', to_field='numero_region', default=None, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    class Meta:
        verbose_name = "universidad"
        verbose_name_plural = 'universidades'
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre

class Region(models.Model):
    id_region = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100, blank=False, verbose_name="Nombre de la región")
    numero_region = models.PositiveIntegerField(unique=True, blank=False, verbose_name="Número de la región")
    letra_region = models.CharField(max_length=5, default=None, verbose_name="Numeros romanos de región")
    slug = models.SlugField(unique=True, default='')
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    class Meta:
        verbose_name = "región"
        verbose_name_plural = 'regiones'
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre