from django.db import models

# Modelo para representar los perfiles de usuario
class PerfilUsuario(models.Model):
    nombre_usuario = models.CharField(max_length=100, unique=True, null=False)
    contrasena = models.CharField(max_length=100, null=False)
    es_administrador = models.BooleanField(default=False)  # Para diferenciar entre empleados y administradores

    def __str__(self):
        return self.nombre_usuario


class ProductoAdmin(models.Model):
    nombre = models.CharField(max_length=255)
    cantidad_vendida = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nombre

class ProductoStock(models.Model):
    nombre = models.CharField(max_length=255)  # Nombre del producto
    cantidad_disponible = models.PositiveIntegerField(default=0)  # Cantidad de producto en stock

    def __str__(self):
        return self.nombre
from django.db import models

class ProductoInventario(models.Model):
    nombre = models.CharField(max_length=255)
    cantidad_disponible = models.PositiveIntegerField(default=0)  # Para gestión de stock
    cantidad_vendida = models.PositiveIntegerField(default=0)  # Para predicción de demanda
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    fecha_ingreso = models.DateField(auto_now_add=True)
    # Agregar otros campos necesarios, como proveedor o categoría, si aplica

    def __str__(self):
        return self.nombre

#Clase Usuario para ingresar como empleado o administrador
class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre_usuario = models.CharField(max_length=100, unique=True)
    contrasena = models.CharField(max_length=255)

    class Meta:
        db_table = 'usuarios'
        managed = False

    def __str__(self):
        return self.nombre_usuario

# Clase Cargo
class Cargo(models.Model):
    id_cargo = models.AutoField(primary_key=True)
    tipo_de_cargo = models.CharField(max_length=100)

    class Meta:
        db_table = 'cargos'  # Coincide con la tabla en PostgreSQL
        managed = False  # Evitar que Django gestione esta tabla

# Clase Empleado
class Empleado(models.Model):
    id_empleado = models.AutoField(primary_key=True)
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    genero = models.CharField(max_length=1, null=True, blank=True)
    direccion = models.CharField(max_length=200, null=True, blank=True)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True, null=True, blank=True)
    fecha_contratacion = models.DateField()
    salario = models.IntegerField()
    estado = models.CharField(max_length=20, default='Activo', null=True, blank=True)
    fecha_termino_contrato = models.DateField(null=True, blank=True)
    id_cargo = models.ForeignKey('Cargo', on_delete=models.SET_NULL, null=True, blank=True)
    id_usuario = models.ForeignKey('Usuario', on_delete=models.SET_NULL, null=True, blank=True, db_column='id_usuario')

    class Meta:
        db_table = 'empleados'
        managed = False


# Clase Categoria
class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre_categoria = models.CharField(max_length=100)

    class Meta:
        db_table = 'categoria'  # Nombre exacto de la tabla en la base de datos
        managed = False  # Django no manejará las migraciones para esta tabla

from django.db import models

# Clase Producto que representa la tabla productos en la base de datos
class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, null=True, blank=True)
    precio_compra = models.IntegerField(null=True, blank=True)
    precio_venta = models.IntegerField(null=True, blank=True)
    stock = models.IntegerField(null=True, blank=True)
    stock_minimo = models.IntegerField(default=0, null=True, blank=True)  # Nuevo atributo
    stock_maximo = models.IntegerField(default=100, null=True, blank=True)  # Nuevo atributo
    nivel_comparativo = models.IntegerField(default=0, null=True, blank=True)  # Nuevo atributo
    cod_barra = models.IntegerField(null=True, blank=True)
    id_categoria = models.IntegerField(null=True, blank=True)  # Podrías cambiar esto a una relación con el modelo Categoria si es aplicable
    proveedor_id = models.IntegerField(null=True, blank=True)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'productos'  # Nombre exacto de la tabla en la base de datos
        managed = False  # Django no manejará las migraciones para esta tabla

    def __str__(self):
        return f"{self.nombre} - Stock: {self.stock}"

# Modelo EstadoSolicitud (para la tabla estados_solicitudes)
class EstadoSolicitud(models.Model):
    descripcion = models.CharField(max_length=50)  # Campo 'descripcion'

    class Meta:
        db_table = 'estados_solicitudes'  # Nombre exacto de la tabla en la base de datos
        managed = False  # Django no gestionará esta tabla

    def __str__(self):
        return self.descripcion

# Modelo Proveedor
class Proveedor(models.Model):
    nombre_completo = models.CharField(max_length=100)
    empresa = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=255, unique=True)
    telefono = models.IntegerField(null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'proveedores'  # Nombre exacto de la tabla en la base de datos
        managed = False  # Django no gestionará esta tabla

    def __str__(self):
        return self.nombre_completo

# Modelo SolicitudProducto
class SolicitudProducto(models.Model):
    codigo_solicitud = models.CharField(max_length=20, unique=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    estado = models.ForeignKey(EstadoSolicitud, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'solicitudes_productos'  # Nombre exacto de la tabla en la base de datos
        managed = False  # Django no gestionará esta tabla

    def __str__(self):
        return self.codigo_solicitud


