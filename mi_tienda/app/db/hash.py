#import psycopg2
#import bcrypt
#from settings import create_connection

def reset_password(username):
    conn = create_connection()
    if conn is None:
        print("No se pudo establecer la conexión con la base de datos.")
        return

    try:
        cursor = conn.cursor()
        
        # Encriptar una contraseña por defecto
        default_password = 'CAMBIAR_CONTRASENA'
        hashed_password = bcrypt.hashpw(default_password.encode('utf-8'), bcrypt.gensalt())
        
        # Actualizar la contraseña a un valor por defecto
        query = "UPDATE usuarios SET contrasena = %s WHERE nombre_usuario = %s"
        cursor.execute(query, (hashed_password.decode('utf-8'), username))
        
        conn.commit()
        print(f"Contraseña para el usuario {username} ha sido restablecida a valor por defecto.")
    except psycopg2.Error as e:
        print(f"Error al actualizar la contraseña: {e}")
    finally:
        conn.close()

# Ejemplo: Restablecer la contraseña para 'pedro'
reset_password('pedro')

def hash_password(password):
    # Generar una sal
    salt = bcrypt.gensalt()
    # Cifrar la contraseña
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def update_password(username, new_password):
    conn = create_connection()
    if conn is None:
        print("No se pudo establecer la conexión con la base de datos.")
        return

    try:
        cursor = conn.cursor()
        
        # Encriptar la nueva contraseña
        hashed_password = hash_password(new_password)
        
        # Actualizar la contraseña en la base de datos
        query = "UPDATE usuarios SET contrasena = %s WHERE nombre_usuario = %s"
        cursor.execute(query, (hashed_password, username))
        
        conn.commit()
        print(f"Contraseña para el usuario {username} actualizada con éxito.")
    except psycopg2.Error as e:
        print(f"Error al actualizar la contraseña: {e}")
    finally:
        conn.close()

update_password('pedro', 'pedro123')
