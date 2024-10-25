from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Usuario(models.Model):
    id_usuario = models.IntegerField(primary_key=True, unique=True)
    nombre_usuario = models.CharField(max_length=100, unique=True)
    contrasena = models.CharField(max_length=100)

    class Meta:
        db_table = 'USUARIOS'  # Indica que el modelo debe usar la tabla existente
        managed = False  # Desactiva la gestión de la tabla por Django

    def save(self, *args, **kwargs):
        if not self.pk or self._state.adding:
            self.contrasena = make_password(self.contrasena)
        super().save(*args, **kwargs)

    def verificar_contrasena(self, contrasena):
        return check_password(contrasena, self.contrasena)

    def _str_(self):
        return self.nombre_usuario
from django.contrib.auth.hashers import make_password

default_password = make_password('temporary_password')


