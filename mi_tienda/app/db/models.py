from settings import create_connection, close_connection
import bcrypt
import psycopg2

# Función para iniciar la conexión a la base de datos
def initialize_db_connection():
    global db_connection
    db_connection = create_connection()
    if db_connection is not None:
        # Aquí podrás ingresar operaciones adicionales si es necesario
        pass

# Función para cerrar la conexión a la base de datos
def close_connection():
    if db_connection:
        db_connection.close()
        print("Conexión a la base de datos cerrada.")


#validando si el usuario existe en la base de datos
def verificar_exitencia(username):
    conn = create_connection()
    if conn is None:
        return False
    try:
        cursor = conn.cursor()
        query = "SELECT 1 FROM usuarios WHERE nombre_usuario = %s"
        cursor.execute(query, (username,))
        exists = cursor.fetchone() is not None
        conn.close()
        return exists
    except psycopg2.Error as e:
        print(f"Error al consultar la base de datos: {e}")
        return False
    
# Variable global para almacenar el id del usuario actual
usuario_actual=None
    
def obtener_nombre_empleado(id_usuario):
    global usuario_actual  # Declarar la variable global

    conn = create_connection()
    if conn is None:
        return None

    try:
        cursor = conn.cursor()
        query = """
            SELECT e.nombre
            FROM empleados e
            WHERE e.id_usuario = %s
        """
        cursor.execute(query, (id_usuario,))
        empleado = cursor.fetchone()
        conn.close()

        if empleado:
            # Asignamos el id_usuario a la variable global usuario_actual
            usuario_actual = id_usuario
            print(f"ID del empleado guardado: {usuario_actual}")  # Verificación
            return empleado[0]  # Devuelve el nombre del empleado
        else:
            print("Empleado no encontrado.")
            return None

    except psycopg2.Error as e:
        print(f"Error al consultar la base de datos: {e}")
        return None



# En model.py
def validacion_usuario(username, password):
    conn = create_connection()
    if conn is None:
        return None, None, None
    try:
        cursor = conn.cursor()
        query = """
            SELECT u.id_usuario, u.contrasena, c.id_cargo
            FROM usuarios u
            JOIN empleados e ON u.id_usuario = e.id_usuario
            JOIN cargos c ON e.id_cargo = c.id_cargo
            WHERE u.nombre_usuario = %s
        """
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        conn.close()

        if user:
            user_id, hashed_password, cargo_id = user
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                # Obtener el nombre del empleado
                nombre_empleado = obtener_nombre_empleado(user_id)
                if nombre_empleado:
                    return user_id, cargo_id, nombre_empleado  # Devuelve id_usuario, cargo_id, nombre_empleado
                else:
                    return None, None, None
            else:
                print("Contraseña incorrecta.")
                return None, None, None
        else:
            print("Usuario no encontrado.")
            return None, None, None

    except psycopg2.Error as e:
        print(f"Error al consultar la base de datos: {e}")
        return None, None, None



# Ejemplo de uso
initialize_db_connection()
close_connection()