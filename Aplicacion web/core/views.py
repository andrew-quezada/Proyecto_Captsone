# Importación de módulos necesarios de Django
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import Usuario, Empleado, ProductoInventario, Producto, Proveedor, SolicitudProducto, EstadoSolicitud, Cargo, VentaProducto
from .forms import EditarProductoForm
from django.contrib.auth import authenticate, login

# Vista para mostrar la página de inicio
def inicio(request):
    return render(request, 'core/inicio.html')

# Vista de validación de usuario: verifica las credenciales de login y redirige según el cargo
def validacion_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # Obtiene el nombre de usuario desde el formulario
        password = request.POST.get('password')  # Obtiene la contraseña desde el formulario
        
        try:
            # Buscar el usuario en la base de datos usando el nombre de usuario
            user = Usuario.objects.get(nombre_usuario=username)
            
            # Verificar si la contraseña es correcta
            if check_password(password, user.contrasena):
                # Autenticación exitosa, se guardan los datos en la sesión
                request.session['usuario_id'] = user.id_usuario
                request.session['nombre_usuario'] = user.nombre_usuario
                
                # Buscar si el usuario está relacionado con un empleado
                empleado = Empleado.objects.filter(id_usuario=user).first()
                
                if empleado:
                    # Obtener el cargo del empleado
                    cargo = empleado.id_cargo
                    
                    # Redirigir dependiendo del cargo (1 = Administrador, 2 = Empleado)
                    if cargo.id_cargo == 1:
                        return redirect('menu_administrador')  # Redirige al menú de administrador
                    elif cargo.id_cargo == 2:
                        return redirect('menu_empleado')  # Redirige al menú de empleado
                    else:
                        messages.error(request, 'Cargo no reconocido.')  # Si el cargo no es reconocido
                        return redirect('inicio')
                else:
                    messages.error(request, 'El usuario no está asociado con un empleado.')  # Si no hay empleado asociado
                    return redirect('inicio')

            else:
                messages.error(request, 'Contraseña incorrecta.')  # Contraseña incorrecta
                return redirect('inicio')
                
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuario no encontrado.')  # Si no existe el usuario
            return redirect('inicio')

    return redirect('inicio')  # Redirige al inicio si no es POST

# Vista para mostrar el menú del empleado con productos más y menos vendidos
def menu_empleado(request):
    # Obtener el producto más vendido y menos vendido
    producto_mas_vendido = Producto.objects.order_by('-stock').first()
    producto_menos_vendido = Producto.objects.order_by('stock').first()

    # Mensajes relacionados con los productos
    mensajes = []
    if producto_mas_vendido:
        mensajes.append({
            'tipo': 'pedido',
            'fecha': producto_mas_vendido.fecha_ingreso,
            'mensaje': f"ID del producto: {producto_mas_vendido.id_producto}"
        })
    if producto_menos_vendido and producto_menos_vendido.stock <= producto_menos_vendido.stock_minimo:
        mensajes.append({
            'tipo': 'stock_critico',
            'fecha': producto_menos_vendido.fecha_ingreso,
            'mensaje': f"ID del producto: {producto_menos_vendido.id_producto}"
        })

    return render(request, 'core/menu_empleado.html', {
        'producto_mas_vendido': producto_mas_vendido,
        'producto_menos_vendido': producto_menos_vendido,
        'mensajes': mensajes
    })

# Vista para mostrar el menú del administrador
def menu_administrador(request):
    return render(request, 'core/menu_administrador.html')

# Vista para gestionar el stock de la tienda mostrando todos los productos
def stock_tienda(request):
    productos_tienda = Producto.objects.all().order_by('id_producto')  # Consulta todos los productos y los ordena por ID
    return render(request, 'core/stock_tienda.html', {'productos_tienda': productos_tienda})

# Vista para mostrar productos solicitados, con relación a su proveedor
def productos_solicitados(request):
    productos_solicitados = SolicitudProducto.objects.select_related('proveedor').all()  # Obtiene los productos solicitados con sus proveedores
    return render(request, 'core/productos_solicitados.html', {'productos_solicitados': productos_solicitados})

# Vista para mostrar la predicción de demanda de productos más y menos vendidos
def prediccion_demanda(request):
    productos = Producto.objects.all()  # Obtiene todos los productos
    # Ordena los productos según la cantidad vendida (nivel_comparativo) para encontrar los más y menos vendidos
    productos_mas_vendidos = productos.order_by('-nivel_comparativo')[:5]
    productos_menos_vendidos = productos.order_by('nivel_comparativo')[:5]

    # Serializa los datos para pasarlos al template
    productos_data_mas_vendidos = [
        {
            'id_producto': producto.id_producto,
            'nombre': producto.nombre,
            'cantidad_vendida': producto.nivel_comparativo,
            'fecha_ingreso': producto.fecha_ingreso
        }
        for producto in productos_mas_vendidos
    ]

    productos_data_menos_vendidos = [
        {
            'id_producto': producto.id_producto,
            'nombre': producto.nombre,
            'cantidad_vendida': producto.nivel_comparativo,
            'fecha_ingreso': producto.fecha_ingreso
        }
        for producto in productos_menos_vendidos
    ]

    return render(request, 'core/prediccion_demanda.html', {
        'productos_mas_vendidos': productos_data_mas_vendidos,
        'productos_menos_vendidos': productos_data_menos_vendidos,
    })

# Vista para gestionar el stock de los productos
def gestion_stock(request):
    productos = Producto.objects.all()  # Consulta todos los productos
    return render(request, 'core/gestion_stock.html', {'productos': productos})

# Vista para editar un producto en el stock
def editar_producto_stock(request, producto_id):
    producto = get_object_or_404(Producto, id_producto=producto_id)  # Obtiene el producto o retorna un error 404
    if request.method == 'POST':
        try:
            # Actualiza los datos del producto con los valores enviados por el formulario
            producto.nombre = request.POST.get('nombre', producto.nombre)
            producto.precio_compra = int(request.POST.get('precio_compra', producto.precio_compra))
            producto.precio_venta = int(request.POST.get('precio_venta', producto.precio_venta))
            producto.stock = int(request.POST.get('stock', producto.stock))
            
            # Guardar los cambios en la base de datos
            producto.save()
            messages.success(request, 'Producto actualizado correctamente.')  # Mensaje de éxito
            return redirect('gestion_stock')  # Redirige a la página de gestión de stock
        except ValueError:
            messages.error(request, 'Por favor, ingrese valores válidos en todos los campos.')  # Mensaje de error

    return render(request, 'core/editar_producto.html', {'producto': producto})  # Muestra el formulario para editar el producto

# Vista para eliminar un producto del stock
def eliminar_producto_stock(request, producto_id):
    producto = get_object_or_404(Producto, id_producto=producto_id)  # Obtiene el producto o retorna un error 404
    if request.method == 'POST':
        producto.delete()  # Elimina el producto
        messages.success(request, 'Producto eliminado correctamente.')  # Mensaje de éxito
        return redirect('gestion_stock')  # Redirige a la página de gestión de stock
    return render(request, 'core/eliminar_producto.html', {'producto': producto})  # Muestra el formulario de confirmación

# Vista para mostrar el formulario de login
def login_view(request):
    return render(request, 'core/login.html')

# Vista para registrar una venta
def registro_venta(request):
    if request.method == 'POST':
        producto_id = request.POST.get('producto')  # Obtiene el producto seleccionado
        cantidad_vendida = int(request.POST.get('cantidad'))  # Obtiene la cantidad vendida
        
        try:
            # Verifica si el producto existe
            producto = Producto.objects.get(id_producto=producto_id)
            
            # Crea un registro en la tabla VentasProductos
            venta = VentasProductos.objects.create(
                producto=producto,
                cantidad_vendida=cantidad_vendida
            )
            
            messages.success(request, f"Venta registrada: {cantidad_vendida} unidades de {producto.nombre}.")  # Mensaje de éxito
        except Producto.DoesNotExist:
            messages.error(request, "El producto no existe.")  # Mensaje de error si el producto no se encuentra
        
        return redirect('registro_venta')  # Redirige a la página de registro de ventas
    else:
        productos = Producto.objects.all()  # Obtiene todos los productos
        return render(request, 'core/registro_venta.html', {'productos': productos})  # Muestra el formulario de registro de ventas
