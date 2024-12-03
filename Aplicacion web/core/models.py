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
    id_usuario = models.AutoField(primary_key=True, db_column='id_usuario')
    nombre_usuario = models.CharField(max_length=100, unique=True, db_column='nombre_usuario')
    contrasena = models.CharField(max_length=255, db_column='contrasena')

    class Meta:
        db_table = 'usuarios'  # Asegura que el nombre coincida con la tabla en PostgreSQL
        managed = False  # Evita que Django intente gestionar la tabla
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return self.nombre_usuario

# Clase Cargo
class Cargo(models.Model):
    id_cargo = models.AutoField(primary_key=True)  
    tipo_de_cargo = models.CharField(max_length=100)  

    class Meta:
        db_table = 'cargos'  # El nombre exacto de la tabla en la base de datos
        managed = False  # Django no manejará la creación/modificación de esta tabla
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'

    def __str__(self):
        return self.tipo_de_cargo

# Clase Empleado
class Empleado(models.Model):
    id_empleado = models.AutoField(primary_key=True, db_column='id_empleado')
    rut = models.CharField(max_length=12, unique=True, db_column='rut')
    nombre = models.CharField(max_length=100, db_column='nombre')
    apellido = models.CharField(max_length=100, db_column='apellido')
    fecha_nacimiento = models.DateField(db_column='fecha_nacimiento')
    genero = models.CharField(max_length=1, null=True, blank=True, db_column='genero')
    direccion = models.CharField(max_length=200, null=True, blank=True, db_column='direccion')
    telefono = models.CharField(max_length=15, null=True, blank=True, db_column='telefono')
    email = models.EmailField(max_length=100, unique=True, null=True, blank=True, db_column='email')
    fecha_contratacion = models.DateField(db_column='fecha_contratacion')
    salario = models.IntegerField(db_column='salario')
    estado = models.CharField(max_length=20, default='Activo', null=True, blank=True, db_column='estado')
    fecha_termino_contrato = models.DateField(null=True, blank=True, db_column='fecha_termino_contrato')
    id_cargo = models.ForeignKey('Cargo', on_delete=models.SET_NULL, null=True, blank=True,db_column='id_cargo')
    id_usuario = models.OneToOneField('Usuario', on_delete=models.SET_NULL,null=True,blank=True,db_column='id_usuario'
    )

    class Meta:
        db_table = 'empleados'  # Nombre exacto de la tabla en la base de datos
        managed = False  # Evita que Django intente gestionar la tabla
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.rut})"


# Clase Categoria
class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre_categoria = models.CharField(max_length=100)

    class Meta:
        db_table = 'categoria'  # Nombre exacto de la tabla en la base de datos
        managed = False  # Django no manejará las migraciones para esta tabla


# Clase Producto que representa la tabla productos en la base de datos
class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, null=True, blank=True)
    precio_compra = models.IntegerField(null=True, blank=True)
    precio_venta = models.IntegerField(null=True, blank=True)
    stock = models.IntegerField(null=True, blank=True)
    cod_barra = models.IntegerField(null=True, blank=True)
    id_categoria = models.IntegerField(null=True, blank=True)  # Puedes cambiar esto a una relación con el modelo Categoria si aplica
    proveedor_id = models.IntegerField(null=True, blank=True)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    stock_minimo = models.IntegerField(default=0, null=True, blank=True)  # Nuevo atributo
    nivel_comparativo = models.IntegerField(default=0, null=True, blank=True)  # Nuevo atributo

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

# Clase venta producto para predicción demanda
class VentaProducto(models.Model):
    id_venta = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(
        'Producto', on_delete=models.CASCADE, db_column='id_producto'
    )
    cantidad_vendida = models.IntegerField(default=0)
    fecha_venta = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'ventas_productos'
        managed = False


class Boleta(models.Model):
    id_boleta = models.AutoField(primary_key=True)  # Clave primaria autoincremental
    fecha = models.DateTimeField(auto_now_add=True)  # Fecha de la boleta, se llena automáticamente
    total = models.DecimalField(max_digits=10, decimal_places=2)  # Total de la boleta con 2 decimales
    id_empleado = models.ForeignKey(
        'Empleado',  # Asume que tienes un modelo `Empleado`
        on_delete=models.SET_NULL,  # Si se elimina el empleado, la referencia queda nula
        null=True,  # Permitir valores nulos
        db_column='id_empleado'
    )

    class Meta:
        db_table = 'boletas'  # Nombre exacto de la tabla en la base de datos
        managed = False  # Django no gestionará esta tabla

    def __str__(self):
        return f"Boleta ID: {self.id_boleta} - Fecha: {self.fecha} - Total: {self.total}"

class DetalleBoleta(models.Model):
    id_detalle_boleta = models.AutoField(primary_key=True)  # Clave primaria autoincremental

    id_boleta = models.ForeignKey(
        'Boleta',  # Asume que tienes un modelo llamado 'Boleta'
        on_delete=models.CASCADE,
        db_column='id_boleta'
    )

    id_producto = models.ForeignKey(
        'Producto',  # Asume que tienes un modelo llamado 'Producto'
        on_delete=models.CASCADE,
        db_column='id_producto'
    )

    cantidad = models.IntegerField(default=0)  # Cantidad del producto en la boleta
    precio_unitario = models.IntegerField(default=0)  # Precio unitario del producto

    class Meta:
        db_table = 'detalle_boleta'  # Nombre exacto de la tabla en tu base de datos
        managed = False  # Indica que Django no gestionará esta tabla

    def __str__(self):
        return f"DetalleBoleta ID: {self.id_detalle_boleta} - Producto ID: {self.id_producto.id_producto} - Cantidad: {self.cantidad}"
