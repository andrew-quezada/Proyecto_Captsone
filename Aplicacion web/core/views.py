# Importación de módulos necesarios de Django
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import Usuario, Empleado, ProductoInventario, Producto, Proveedor, SolicitudProducto, EstadoSolicitud, Cargo, VentaProducto, Boleta, DetalleBoleta
from .forms import EditarProductoForm, ProveedorForm
from django.contrib.auth import authenticate, login
from django.utils import timezone
from django.db.models import Sum, F
from prophet import Prophet
from django.utils.timezone import now
from decimal import Decimal  # Agregado
from django.db import transaction  # Para transacciones seguras
from datetime import datetime  # Asegúrate de incluir esta línea
import pandas as pd
import matplotlib.pyplot as plt
import io
import urllib, base64


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

    # Calcular las ventas del día actual
    ventas_dia = DetalleBoleta.objects.filter(id_boleta__fecha__date=timezone.now().date()) \
        .values('id_producto') \
        .annotate(total_vendido=Sum('cantidad')) \
        .order_by('-total_vendido')
    producto_mas_vendido_hoy = Producto.objects.get(id_producto=ventas_dia[0]['id_producto']) if ventas_dia else None

    # Productos con bajo stock
    productos_bajo_stock = Producto.objects.filter(stock__lte=F('stock_minimo'))

    # Productos vendidos con stock insuficiente
    ventas_stock_insuficiente = DetalleBoleta.objects.filter(
        id_producto__stock__lt=F('cantidad')
    ).values('id_producto').annotate(total_vendido=Sum('cantidad'))

    # Total de ventas del empleado (si aplica autenticación)
    empleado = request.user  # Suponiendo que el empleado está autenticado
    total_ventas_empleado = Boleta.objects.filter(
        id_empleado=empleado.id,
        fecha__date=timezone.now().date()
    ).aggregate(total=Sum('total'))['total'] or 0

    # Mensajes relacionados con los productos
    mensajes = []
    # Mensaje del producto menos vendido con stock crítico
    if producto_menos_vendido and producto_menos_vendido.stock <= producto_menos_vendido.stock_minimo:
        mensajes.append({
            'tipo': 'stock_critico',
            'fecha': producto_menos_vendido.fecha_ingreso,
            'mensaje': f"Producto con stock crítico: ID {producto_menos_vendido.id_producto}."
        })
    # Mensajes de productos con bajo stock
    for producto in productos_bajo_stock:
        mensajes.append({
            'tipo': 'stock_bajo',
            'fecha': producto.fecha_ingreso,
            'mensaje': f"El producto {producto.nombre} tiene un stock crítico ({producto.stock} unidades)."
        })
    # Resumen de ventas del empleado
    mensajes.append({
        'tipo': 'resumen',
        'fecha': timezone.now().date(),
        'mensaje': f"Hoy has generado un total de ventas por ${total_ventas_empleado}."
    })

    # Renderizar la vista con el contexto
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
    # Obtener el producto seleccionado
    producto_id = request.GET.get('producto_id')
    productos = Producto.objects.all()  # Lista de productos para el formulario

    # Filtrar datos dependiendo del producto seleccionado
    if producto_id:
        ventas = (
            DetalleBoleta.objects.filter(id_producto=producto_id)
            .values('id_boleta__fecha')  # Obtener la fecha desde la tabla boletas
            .annotate(total_vendida=Sum('cantidad'))  # Sumar las cantidades vendidas
            .order_by('id_boleta__fecha')
        )
    else:
        ventas = (
            DetalleBoleta.objects.values('id_boleta__fecha')  # Todas las boletas
            .annotate(total_vendida=Sum('cantidad'))
            .order_by('id_boleta__fecha')
        )

    # Convertir los datos a DataFrame para trabajar con Prophet
    df = pd.DataFrame(list(ventas))
    if df.empty or len(df) < 2:
        return render(request, 'core/prediccion_demanda.html', {
            'prediccion_futura': None,
            'error': 'No hay datos suficientes para realizar la predicción.',
            'productos': productos,
        })

    # Renombrar columnas para Prophet
    df.rename(columns={'id_boleta__fecha': 'ds', 'total_vendida': 'y'}, inplace=True)

    # Crear y ajustar el modelo Prophet
    model = Prophet()
    model.fit(df)

    # Generar predicción
    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)

    # Generar gráfico
    plt.figure(figsize=(10, 6))
    plt.plot(df['ds'], df['y'], label='Datos históricos')
    plt.plot(forecast['ds'], forecast['yhat'], label='Predicción', color='orange')
    plt.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], color='gray', alpha=0.2)
    plt.title('Predicción de Demanda')
    plt.xlabel('Fecha')
    plt.ylabel('Demanda')
    plt.legend()

    # Convertir gráfico a base64
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    return render(request, 'core/prediccion_demanda.html', {
        'prediccion_futura': forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_dict(orient='records'),
        'grafico': image_base64,
        'productos': productos,
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
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id_producto=producto_id)
    if request.method == 'POST':  # Asegúrate de que la eliminación se haga con una solicitud POST
        producto.delete()
        messages.success(request, 'Producto eliminado correctamente.')
        return redirect('gestion_stock')
    return render(request, 'core/eliminar_producto.html', {'producto': producto})
    
# Vista para mostrar el formulario de login
def login_view(request):
    return render(request, 'core/login.html')

# Vista para registrar una venta
def registro_venta(request):
    if request.method == 'POST':
        producto_id = request.POST.get('id_producto')
        cantidad_vendida = request.POST.get('cantidad')
        fecha_boleta = request.POST.get('fecha_boleta')  # Recibir fecha desde el formulario

        # Validar entrada
        if not producto_id or not cantidad_vendida.isdigit() or not fecha_boleta:
            messages.error(request, "Datos inválidos. Verifique el formulario.")
            return redirect('registro_venta')

        try:
            # Intentar convertir la fecha_boleta a un objeto datetime
            fecha_boleta = datetime.strptime(fecha_boleta, '%Y-%m-%d')
        except ValueError:
            messages.error(request, "La fecha ingresada no es válida. Use el formato YYYY-MM-DD.")
            return redirect('registro_venta')

        cantidad_vendida = int(cantidad_vendida)

        # Obtener producto o error 404
        producto = get_object_or_404(Producto, id_producto=producto_id)

        # Verificar stock
        if producto.stock < cantidad_vendida:
            messages.error(
                request,
                f"Stock insuficiente: {producto.stock} unidades disponibles."
            )
            return redirect('registro_venta')

        try:
            # Realizar todo en una transacción para consistencia
            with transaction.atomic():
                # Actualizar stock
                producto.stock -= cantidad_vendida
                producto.save()

                # Crear boleta usando la fecha proporcionada
                boleta = Boleta.objects.create(
                    fecha=fecha_boleta,  # Se asigna la fecha recibida desde el formulario
                    total=Decimal(0),  # Inicialmente en 0, se calculará
                    id_empleado=request.user.id  # Asumiendo autenticación
                )

                # Registrar detalle de boleta
                DetalleBoleta.objects.create(
                    id_boleta=boleta,
                    id_producto=producto,
                    cantidad=cantidad_vendida,
                    precio_unitario=producto.precio_venta
                )

                # Calcular y actualizar total de la boleta
                boleta.total += Decimal(cantidad_vendida) * producto.precio_venta
                boleta.save()

            messages.success(
                request,
                f"Venta registrada: {cantidad_vendida} unidades de {producto.nombre}."
            )
        except Exception as e:
            messages.error(request, f"Error al registrar la venta: {e}")

        return redirect('registro_venta')

    # Renderizar formulario
    productos = Producto.objects.all()
    return render(request, 'core/registro_venta.html', {'productos': productos})

def listar_proveedores(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'core/listar_proveedores.html', {'proveedores': proveedores})

def editar_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, id=proveedor_id)
    
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            return redirect('listar_proveedores')  # Redirige a la lista de proveedores
    else:
        form = ProveedorForm(instance=proveedor)
    
    return render(request, 'core/editar_proveedor.html', {'form': form, 'proveedor': proveedor})