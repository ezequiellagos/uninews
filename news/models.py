from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Noticia(models.Model):
    id_noticia = models.IntegerField(primary_key=True)
    titulo = models.CharField(max_length=200)
    titulo_busqueda = models.CharField(max_length=200, default='')
    bajada = models.TextField()
    bajada_busqueda = models.TextField(default='')
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


from django.db import models
from cities_light.models import City
from django.utils.text import slugify

# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=400)
    summary = models.TextField()
    content = models.TextField(blank=True)
    pub_date = models.DateTimeField()
    url_source = models.URLField(max_length=400)
    url_image = models.URLField(max_length=400)
    slug = models.SlugField(max_length=450, unique=True)
    active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    search_title = models.CharField(max_length=400)
    search_summary = models.TextField(blank=True)
    search_content = models.TextField(blank=True)
    visitor_counter = models.IntegerField(default=0)
    is_legacy = models.BooleanField(default=False)
    university = models.ForeignKey('University', on_delete=models.PROTECT)
    categories = models.ManyToManyField('Category', related_name='news', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Noticia'
        verbose_name_plural = 'Noticias'
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.title) + '-' + str(self.pub_date.year) + '-' + str(self.pub_date.month) + '-' + str(self.pub_date.day) + '-' + str(self.university.alias))
        super(News, self).save(*args, **kwargs)
        

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    active = models.BooleanField(default=True)
    description = models.CharField(max_length=200, blank=True)
    is_legacy = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

class University(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    alias = models.CharField(max_length=10)
    active = models.BooleanField(default=True)
    is_public = models.BooleanField(default=True)
    image = models.ImageField(upload_to='universities')
    url_web = models.URLField(blank=True)
    location = models.ForeignKey(City, on_delete=models.PROTECT)
    associations = models.ManyToManyField('Association', related_name='universities', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Universidad'
        verbose_name_plural = 'Universidades'
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(University, self).save(*args, **kwargs)

class Association(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    alias = models.CharField(max_length=10)
    url_web = models.URLField(blank=True)
    url_image = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Asociación'
        verbose_name_plural = 'Asociaciónes'
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Association, self).save(*args, **kwargs)

