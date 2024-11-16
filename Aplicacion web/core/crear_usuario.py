import os
import sys
import django

# Agrega la ruta a la raíz del proyecto
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configura el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PanaderiaMadrilena.settings')
django.setup()

from django.contrib.auth.hashers import make_password
from core.models import Usuario  # Cambiar 'Usuarios' por 'Usuario'

def crear_usuario(nombre_usuario, contrasena):
    try:
        # Hashear la contraseña usando el método de Django
        contrasena_hacheada = make_password(contrasena)
        
        # Crear el usuario en la base de datos
        usuario = Usuario.objects.create(
            nombre_usuario=nombre_usuario,
            contrasena=contrasena_hacheada
        )
        
        print("Usuario creado exitosamente.")
        return usuario

    except Exception as e:
        print(f"Error al crear el usuario: {e}")
        return None

# Crear un nuevo usuario
nuevo_usuario = crear_usuario("carlos", "123")
nuevo_usuario = crear_usuario("juan", "contrasena123")