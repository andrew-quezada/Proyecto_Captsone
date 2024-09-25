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
    
def validacion_usuario(username, password):
    conn = create_connection()
    if conn is None:
        return None, None
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
            # Verificar la contraseña ingresada contra el hash almacenado
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                return user_id, cargo_id  # Devuelve (id_usuario, id_cargo)
            else:
                print("Contraseña incorrecta.")
                return None, None
        else:
            print("Usuario no encontrado.")
            return None, None
            
    except psycopg2.Error as e:
        print(f"Error al consultar la base de datos: {e}")
        return None, None



# Ejemplo de uso
initialize_db_connection()
close_connection()