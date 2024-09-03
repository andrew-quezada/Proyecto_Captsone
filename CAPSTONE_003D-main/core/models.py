from django.db import models

# Create your models here.

from django.db import models

class Usuario(models.Model):
    nombreusuario = models.CharField(max_length=100, unique=True, null=False)
    contrasena = models.CharField(max_length=100, null=False)
    es_admin = models.BooleanField(default=False)  # Asegúrate de que este campo esté incluido

    def __str__(self):
        return self.nombreusuario

