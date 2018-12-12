from django.db import models

# Create your models here.
class Noticia(models.Model):
    id_noticia = models.IntegerField(primary_key=True)
    titulo = models.CharField(max_length=200)
    bajada = models.TextField()
    fecha = models.DateField(blank=True, null=True)
    link_noticia = models.CharField(max_length=200)
    link_recurso = models.CharField(max_length=200)
    id_universidad = models.ForeignKey('Universidad', default=None, on_delete=models.CASCADE)
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
    region = models.CharField(max_length=2)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    class Meta:
        verbose_name = "universidad"
        verbose_name_plural = 'universidades'
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre
