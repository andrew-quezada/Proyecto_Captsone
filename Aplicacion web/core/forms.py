# forms.py

from django import forms
from .models import ProductoInventario, Proveedor

class EditarProductoForm(forms.ModelForm):
    class Meta:
        model = ProductoInventario
        fields = ['nombre', 'cantidad_disponible']  # Campos que quieres permitir editar


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre_completo', 'empresa', 'email', 'telefono']
        widgets = {
            'nombre_completo': forms.TextInput(attrs={'class': 'form-control'}),
            'empresa': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.NumberInput(attrs={'class': 'form-control'}),
        }