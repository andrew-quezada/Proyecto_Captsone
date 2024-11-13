from django.db import models

# Modelo para representar los perfiles de usuario
class PerfilUsuario(models.Model):
    nombre_usuario = models.CharField(max_length=100, unique=True, null=False)
    contrasena = models.CharField(max_length=100, null=False)
    es_administrador = models.BooleanField(default=False)  # Para diferenciar entre empleados y administradores

    def __str__(self):
        return self.nombre_usuario

# Modelo para representar los productos
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    cantidad_disponible = models.IntegerField()

    def __str__(self):
        return self.nombre

# Modelo para representar los proveedores
class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

# Modelo para representar los productos solicitados
class ProductosSolicitados(models.Model):
    nombre_producto = models.CharField(max_length=200)
    cantidad = models.PositiveIntegerField()
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name="productos_solicitados")

    def __str__(self):
        return f"{self.nombre_producto} - {self.cantidad} unidades"

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


