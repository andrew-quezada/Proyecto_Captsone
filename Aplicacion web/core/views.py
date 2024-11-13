from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import PerfilUsuario, Producto, ProductoAdmin, ProductoStock, ProductoInventario
from .forms import EditarProductoForm  # Este será el formulario de edición

def inicio(request):
    return render(request, 'core/inicio.html')

def validar_usuario(request):
    if request.method == "POST":
        nombre_usuario = request.POST.get('nombre_usuario')
        contrasena = request.POST.get('contrasena')

        try:
            usuario = PerfilUsuario.objects.get(nombre_usuario=nombre_usuario)
            if usuario.contrasena == contrasena:
                if usuario.es_administrador:
                    return redirect('menu_administrador')
                else:
                    return redirect('menu_empleado')
            else:
                messages.error(request, "Nombre de usuario o contraseña incorrectos.")
        except PerfilUsuario.DoesNotExist:
            messages.error(request, "Nombre de usuario o contraseña incorrectos.")
    
    return render(request, 'core/inicio.html')

# Vistas de los menús
def menu_empleado(request):
    return render(request, 'core/menu_empleado.html')

def menu_administrador(request):
    return render(request, 'core/menu_administrador.html')

# Vista para "Stock Tienda"
def stock_tienda(request):
    productos_tienda = Producto.objects.all()  # Obtiene todos los productos disponibles
    return render(request, 'core/stock_tienda.html', {'productos_tienda': productos_tienda})


# Vista para "Productos Solicitados"
def productos_solicitados(request):
    # Aquí puedes agregar lógica para obtener datos de los productos solicitados
    # Por ejemplo, podrías hacer una consulta a la base de datos para obtener los productos que han sido pedidos

    # Renderizar la plantilla de productos_solicitados.html
    return render(request, 'core/productos_solicitados.html')

# Vista para la gestión de productos
def gestion_stock(request):
    # Lógica para obtener datos de productos, inventario, etc.
    return render(request, 'gestion_stock.html')

# Vista para la predicción de demanda del administrador
def prediccion_demanda(request):
    # Obtiene todos los productos de ProductoInventario
    productos_admin = ProductoInventario.objects.all()

    # Serialización de los productos en un formato que se pueda utilizar fácilmente en JavaScript
    productos_mas_vendidos = sorted(productos_admin, key=lambda x: x.cantidad_vendida, reverse=True)
    productos_menos_vendidos = sorted(productos_admin, key=lambda x: x.cantidad_vendida)

    # Convertir los productos en formato de lista de diccionarios para JavaScript
    productos_data_mas_vendidos = [
        {
            'nombre': producto.nombre,
            'cantidad_vendida': producto.cantidad_vendida,
        }
        for producto in productos_mas_vendidos
    ]
    productos_data_menos_vendidos = [
        {
            'nombre': producto.nombre,
            'cantidad_vendida': producto.cantidad_vendida,
        }
        for producto in productos_menos_vendidos
    ]

    return render(request, 'core/prediccion_demanda.html', {
        'productos_mas_vendidos': productos_data_mas_vendidos,
        'productos_menos_vendidos': productos_data_menos_vendidos
    })

# Vista para la gestión de stock del administrador
def gestion_stock(request):
    productos_stock = ProductoInventario.objects.all()  # Usar el modelo ProductoInventario
    return render(request, 'core/gestion_stock.html', {'productos_stock': productos_stock})


def editar_producto_stock(request, producto_id):
    producto = get_object_or_404(ProductoInventario, id=producto_id)
    
    if request.method == 'POST':
        form = EditarProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()  # Guarda los cambios en el producto
            return redirect('gestion_stock')  # Redirige a la página de gestión de stock
    else:
        form = EditarProductoForm(instance=producto)
    
    return render(request, 'core/editar_producto.html', {'form': form, 'producto': producto})

def eliminar_producto_stock(request, producto_id):
    producto = get_object_or_404(ProductoInventario, id=producto_id)
    
    if request.method == 'POST':
        producto.delete()  # Elimina el producto
        return redirect('gestion_stock')  # Redirige a la página de gestión de stock
    
    return render(request, 'core/eliminar_producto.html', {'producto': producto})