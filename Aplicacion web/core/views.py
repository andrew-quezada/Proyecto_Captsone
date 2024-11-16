from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import Usuario, Empleado, ProductoInventario, Producto, Proveedor, SolicitudProducto, EstadoSolicitud, Cargo
from .forms import EditarProductoForm
from django.contrib.auth import authenticate, login

def inicio(request):
    return render(request, 'core/inicio.html')


def validacion_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = Usuario.objects.get(nombre_usuario=username)
            
            # Verificar la contraseña usando check_password
            if check_password(password, user.contrasena):
                # Autenticación exitosa
                request.session['usuario_id'] = user.id_usuario
                request.session['nombre_usuario'] = user.nombre_usuario
                
                # Determina la redirección según el rol
                if Empleado.objects.filter(id_usuario=user).exists():
                    return redirect('menu_empleado')
                else:
                    return redirect('menu_administrador')
            else:
                messages.error(request, 'Contraseña incorrecta.')
                return redirect('inicio')
                
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuario no encontrado.')
            return redirect('inicio')

    return redirect('inicio')

# El resto de tus vistas...
def menu_empleado(request):
    productos = Producto.objects.all()
    return render(request, 'core/menu_empleado.html', {'productos': productos})

def menu_administrador(request):
    return render(request, 'core/menu_administrador.html')

def stock_tienda(request):
    productos_tienda = Producto.objects.all()  # Consulta todos los productos en la tabla
    return render(request, 'core/stock_tienda.html', {'productos_tienda': productos_tienda})

# Vista para mostrar productos solicitados y sus detalles
def productos_solicitados(request):
    # Obtén todos los productos solicitados, junto con sus proveedores y estados, para optimizar el acceso en la plantilla
    productos_solicitados = SolicitudProducto.objects.select_related('proveedor', 'estado').all()
    
    # Renderizar los productos solicitados a la plantilla
    return render(request, 'core/productos_solicitados.html', {
        'productos_solicitados': productos_solicitados
    })

def prediccion_demanda(request):
    productos_admin = ProductoInventario.objects.all()
    productos_mas_vendidos = sorted(productos_admin, key=lambda x: x.cantidad_vendida, reverse=True)
    productos_menos_vendidos = sorted(productos_admin, key=lambda x: x.cantidad_vendida)

    productos_data_mas_vendidos = [{'nombre': p.nombre, 'cantidad_vendida': p.cantidad_vendida} for p in productos_mas_vendidos]
    productos_data_menos_vendidos = [{'nombre': p.nombre, 'cantidad_vendida': p.cantidad_vendida} for p in productos_menos_vendidos]

    return render(request, 'core/prediccion_demanda.html', {
        'productos_mas_vendidos': productos_data_mas_vendidos,
        'productos_menos_vendidos': productos_data_menos_vendidos
    })

def gestion_stock(request):
    productos_stock = ProductoInventario.objects.all()
    return render(request, 'core/gestion_stock.html', {'productos_stock': productos_stock})

def editar_producto_stock(request, producto_id):
    producto = get_object_or_404(ProductoInventario, id=producto_id)
    if request.method == 'POST':
        form = EditarProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('gestion_stock')
    else:
        form = EditarProductoForm(instance=producto)
    return render(request, 'core/editar_producto.html', {'form': form, 'producto': producto})

def eliminar_producto_stock(request, producto_id):
    producto = get_object_or_404(ProductoInventario, id=producto_id)
    if request.method == 'POST':
        producto.delete()
        return redirect('gestion_stock')
    return render(request, 'core/eliminar_producto.html', {'producto': producto})

def login_view(request):
    return render(request, 'core/login.html')
