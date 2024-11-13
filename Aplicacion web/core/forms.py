# forms.py

from django import forms
from .models import ProductoInventario

class EditarProductoForm(forms.ModelForm):
    class Meta:
        model = ProductoInventario
        fields = ['nombre', 'cantidad_disponible']  # Campos que quieres permitir editar