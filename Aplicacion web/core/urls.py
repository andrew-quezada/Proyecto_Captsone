from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('validar_usuario/', views.validar_usuario, name='validar_usuario'),
    path('menu_empleado/', views.menu_empleado, name='menu_empleado'),
    path('menu_administrador/', views.menu_administrador, name='menu_administrador'),
    path('logout/', auth_views.LogoutView.as_view(next_page='inicio'), name='logout'),
    path('productos_solicitados/', views.productos_solicitados, name='productos_solicitados'),
    path('stock_tienda/', views.stock_tienda, name='stock_tienda'),
    path('gestion_stock/', views.gestion_stock, name='gestion_stock'),
    path('prediccion_demanda/', views.prediccion_demanda, name='prediccion_demanda'),
    path('editar_producto/<int:producto_id>/', views.editar_producto_stock, name='editar_producto_stock'),
    path('eliminar_producto/<int:producto_id>/', views.eliminar_producto_stock, name='eliminar_producto_stock'),
]
