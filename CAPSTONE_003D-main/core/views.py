from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Usuario

def index(request):
    return render(request, 'core/index.html')

def validar_usuario(request):
    if request.method == "POST":
        nombre_usuario = request.POST.get('username')
        contrasena = request.POST.get('password')

        try:
            usuario = Usuario.objects.get(nombreusuario=nombre_usuario)
            if usuario.contrasena == contrasena:
                if usuario.es_admin:
                    return redirect('menu_admin')
                else:
                    return redirect('menu_empleado')
            else:
                messages.error(request, "Nombre de usuario o contraseña incorrectos.")
        except Usuario.DoesNotExist:
            messages.error(request, "Nombre de usuario o contraseña incorrectos.")
    
    return render(request, 'core/index.html')

# Otras vistas
def menu_empleado(request):
    return render(request, 'core/menu_empleado.html')

def menu_admin(request):
    return render(request, 'core/menu_admin.html')

def recuperacion(request):
    return render(request, 'core/recuperacion.html')

def recibido(request):
    return render(request, 'core/recibido.html')
