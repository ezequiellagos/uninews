from django.db import models

# Create your models here.
class Email(models.Model):
    id = models.IntegerField(primary_key=True)
    email = models.CharField(max_length=200, unique=True)
    register = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    class Meta:
        verbose_name = "correo"
        verbose_name_plural = 'correos'
        ordering = ["register"]

    def __str__(self):
        return self.email