from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Usuario

def index(request):
    if request.method == "POST":
        nombre_usuario = request.POST.get('username')
        contrasena = request.POST.get('password')

        try:
            usuario = Usuario.objects.get(nombre_usuario=nombre_usuario)
            if usuario.verificar_contrasena(contrasena):
                return redirect('core/menu')
            else:
                messages.error(request, "Nombre de usuario o contraseña incorrectos.")
        except Usuario.DoesNotExist:
            messages.error(request, "Nombre de usuario o contraseña incorrectos.")
    
    return render(request, 'core/index.html')


def menu(request):
    return render(request, 'core/menu.html')

def recuperacion(request):
    return render(request, 'core/recuperacion.html')

def recibido(request):
    return render(request, 'core/recibido.html')

from django.urls import path
from . import views

urlpatterns = [
    path('prueba/', views.prueba_usuarios, name='prueba_usuarios'),
]
