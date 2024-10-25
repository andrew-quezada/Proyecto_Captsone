from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Esto apunta a la función index en views.py
    path('menu/', views.menu, name='menu'),
    path('recuperacion/', views.recuperacion, name='recuperacion'),
    path('recibido/', views.recibido, name='recibido')
]
