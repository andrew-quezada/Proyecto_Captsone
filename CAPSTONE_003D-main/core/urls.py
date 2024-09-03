from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Ruta para la página de inicio (login)
    path('validar_usuario/', views.validar_usuario, name='validar_usuario'),  # URL para la validación del usuario
    path('menu_empleado/', views.menu_empleado, name='menu_empleado'),  # Ruta para el menú de empleados
    path('menu_admin/', views.menu_admin, name='menu_admin'),  # Ruta para el menú de administradores
    path('recuperacion/', views.recuperacion, name='recuperacion'),
    path('recibido/', views.recibido, name='recibido'),
]
